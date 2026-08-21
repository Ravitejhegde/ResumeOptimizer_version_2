from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.billing.providers.stripe.webhook import StripeWebhook
from app.database.models.payment_transaction import PaymentTransaction
from app.database.models.subscription import Subscription
from app.database.repositories.order_repository import OrderRepository
from app.database.repositories.payment_transaction_repository import (
    PaymentTransactionRepository,
)
from app.database.repositories.subscription_repository import (
    SubscriptionRepository,
)
from app.database.repositories.webhook_event_repository import (
    WebhookEventRepository,
)


logger = logging.getLogger(__name__)


class WebhookService:
    """
    Handles Stripe webhook business logic.

    Responsibilities
    ----------------
    - Verify Stripe webhook signatures.
    - Prevent duplicate webhook processing.
    - Process checkout completion.
    - Record successful payment transactions.
    - Create/update local subscriptions.
    - Synchronize recurring subscription state.
    - Handle failed invoices.
    - Handle subscription cancellation.

    This service contains billing business logic.

    HTTP concerns belong to:
        app.billing.routes.webhook

    Stripe-specific webhook parsing belongs to:
        app.billing.providers.stripe.webhook
    """

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

        self.webhook = StripeWebhook()

        self.orders = OrderRepository(db)

        self.transactions = PaymentTransactionRepository(
            db
        )

        self.subscriptions = SubscriptionRepository(
            db
        )

        self.events = WebhookEventRepository(
            db
        )

    # ==========================================================
    # Main Handler
    # ==========================================================

    def process(
        self,
        payload: bytes,
        signature: str,
    ) -> dict:
        """
        Verify and process a Stripe webhook event.

        The webhook event is recorded only after successful
        business processing.

        This is important because Stripe retries failed
        webhook deliveries.
        """

        # ------------------------------------------------------
        # Verify Stripe signature
        # ------------------------------------------------------

        event = self.webhook.verify(
            payload,
            signature,
        )

        event_id = event.get("id")
        event_type = event.get("type")

        if not event_id:
            raise ValueError(
                "Stripe webhook event is missing an event ID."
            )

        if not event_type:
            raise ValueError(
                "Stripe webhook event is missing an event type."
            )

        # ------------------------------------------------------
        # Duplicate protection
        # ------------------------------------------------------

        if self.events.exists(
            "stripe",
            event_id,
        ):
            logger.info(
                "Ignoring duplicate Stripe webhook: %s",
                event_id,
            )

            return {
                "duplicate": True,
                "event_id": event_id,
            }

        # ------------------------------------------------------
        # Route event
        # ------------------------------------------------------

        try:

            if self.webhook.is_checkout_completed(
                event
            ):
                self._checkout_completed(
                    event
                )

            elif self.webhook.is_invoice_paid(
                event
            ):
                self._invoice_paid(
                    event
                )

            elif self.webhook.is_invoice_failed(
                event
            ):
                self._invoice_failed(
                    event
                )

            elif self.webhook.is_subscription_updated(
                event
            ):
                self._subscription_updated(
                    event
                )

            elif self.webhook.is_subscription_deleted(
                event
            ):
                self._subscription_deleted(
                    event
                )

            else:
                logger.info(
                    "Ignoring unsupported Stripe webhook event: %s",
                    event_type,
                )

            # --------------------------------------------------
            # Record event only after successful processing
            # --------------------------------------------------

            self.events.create(
                provider="stripe",
                event_id=event_id,
                event_type=event_type,
            )

            logger.info(
                "Stripe webhook processed successfully: %s",
                event_type,
            )

            return {
                "processed": True,
                "event": event_type,
                "event_id": event_id,
            }

        except Exception:
            self.db.rollback()

            logger.exception(
                "Stripe webhook processing failed. "
                "event_id=%s event_type=%s",
                event_id,
                event_type,
            )

            raise

    # ==========================================================
    # Checkout Completed
    # ==========================================================

    def _checkout_completed(
        self,
        event: dict,
    ) -> None:
        """
        Finalize a successful Stripe Checkout Session.

        Flow:

            Checkout Session
                    ↓
                Local Order
                    ↓
            Payment Transaction
                    ↓
              Subscription
        """

        data = self.webhook.data(
            event
        )

        # ------------------------------------------------------
        # Find local order
        # ------------------------------------------------------

        order_id = (
            data.get("client_reference_id")
            or data.get("metadata", {}).get(
                "order_id"
            )
        )

        if not order_id:
            raise ValueError(
                "Checkout session does not contain an order ID."
            )

        order = self.orders.get(
            order_id
        )

        if order is None:
            raise ValueError(
                f"Order not found: {order_id}"
            )

        # ------------------------------------------------------
        # Verify payment status
        # ------------------------------------------------------

        payment_status = data.get(
            "payment_status"
        )

        if payment_status != "paid":
            logger.info(
                "Checkout session is not paid yet. "
                "Order=%s status=%s",
                order.id,
                payment_status,
            )
            return

        # ------------------------------------------------------
        # Store Checkout Session ID
        # ------------------------------------------------------

        checkout_session_id = data.get(
            "id"
        )

        if checkout_session_id:
            order.provider_order_id = (
                checkout_session_id
            )

        # ------------------------------------------------------
        # Mark order completed
        # ------------------------------------------------------

        if order.status != "completed":
            self.orders.mark_completed(
                order
            )

        # ------------------------------------------------------
        # Payment transaction
        # ------------------------------------------------------

        payment_intent_id = data.get(
            "payment_intent"
        )

        if not payment_intent_id:
            raise ValueError(
                "Checkout session does not contain "
                "a Stripe payment intent ID."
            )

        transaction = (
            self.transactions
            .get_by_provider_transaction(
                payment_intent_id
            )
        )

        if transaction is None:

            transaction = PaymentTransaction(
                order_id=order.id,
                provider="stripe",
                provider_transaction_id=(
                    payment_intent_id
                ),
                amount=order.amount,
                currency=order.currency.upper(),
                status="paid",
            )

            self.transactions.create(
                transaction
            )

        elif not transaction.is_successful:

            self.transactions.mark_successful(
                transaction
            )

        # ------------------------------------------------------
        # Stripe subscription ID
        # ------------------------------------------------------

        stripe_subscription_id = data.get(
            "subscription"
        )

        if not stripe_subscription_id:
            raise ValueError(
                "Checkout session does not contain "
                "a Stripe subscription ID."
            )

        # ------------------------------------------------------
        # Retrieve authoritative subscription state
        # ------------------------------------------------------

        stripe_subscription = (
            self.webhook.subscription(
                stripe_subscription_id
            )
        )

        self._sync_subscription(
            order=order,
            stripe_subscription=stripe_subscription,
        )

        logger.info(
            "Checkout completed successfully. "
            "order=%s subscription=%s",
            order.id,
            stripe_subscription_id,
        )

    # ==========================================================
    # Subscription Synchronization
    # ==========================================================

    def _sync_subscription(
        self,
        *,
        order,
        stripe_subscription: dict,
    ) -> Subscription:
        """
        Synchronize a local subscription with Stripe state.

        Creates the local subscription if it does not exist.
        Otherwise updates the existing subscription.
        """

        stripe_subscription_id = (
            stripe_subscription.get("id")
        )

        if not stripe_subscription_id:
            raise ValueError(
                "Stripe subscription is missing its ID."
            )

        # ------------------------------------------------------
        # Billing period
        # ------------------------------------------------------

        period_start = (
            stripe_subscription.get(
                "current_period_start"
            )
        )

        period_end = (
            stripe_subscription.get(
                "current_period_end"
            )
        )

        if not period_start:
            raise ValueError(
                "Stripe subscription is missing "
                "current_period_start."
            )

        if not period_end:
            raise ValueError(
                "Stripe subscription is missing "
                "current_period_end."
            )

        starts_at = datetime.fromtimestamp(
            period_start,
            tz=timezone.utc,
        )

        expires_at = datetime.fromtimestamp(
            period_end,
            tz=timezone.utc,
        )

        # ------------------------------------------------------
        # Stripe status → local status
        # ------------------------------------------------------

        stripe_status = (
            stripe_subscription.get(
                "status"
            )
        )

        status_map = {
            "active": "active",
            "trialing": "active",
            "past_due": "past_due",
            "unpaid": "unpaid",
            "canceled": "cancelled",
            "incomplete": "incomplete",
            "incomplete_expired": "expired",
        }

        local_status = status_map.get(
            stripe_status,
            stripe_status or "active",
        )

        # ------------------------------------------------------
        # Auto renewal
        # ------------------------------------------------------

        auto_renew = not bool(
            stripe_subscription.get(
                "cancel_at_period_end",
                False,
            )
        )

        # ------------------------------------------------------
        # Cancellation timestamp
        # ------------------------------------------------------

        cancelled_at = None

        canceled_at = stripe_subscription.get(
            "canceled_at"
        )

        if canceled_at:
            cancelled_at = datetime.fromtimestamp(
                canceled_at,
                tz=timezone.utc,
            )

        # ------------------------------------------------------
        # Find existing subscription
        # ------------------------------------------------------

        subscription = (
            self.subscriptions
            .get_by_provider_subscription_id(
                stripe_subscription_id
            )
        )

        if subscription is None:
            subscription = (
                self.subscriptions.get_by_order(
                    order.id
                )
            )

        # ------------------------------------------------------
        # Create new subscription
        # ------------------------------------------------------

        if subscription is None:

            subscription = Subscription(
                user_id=order.user_id,
                order_id=order.id,
                provider_subscription_id=(
                    stripe_subscription_id
                ),
                status=local_status,
                auto_renew=auto_renew,
                starts_at=starts_at,
                expires_at=expires_at,
                cancelled_at=cancelled_at,
            )

            self.subscriptions.create(
                subscription
            )

            logger.info(
                "Created local subscription. "
                "user=%s subscription=%s",
                order.user_id,
                stripe_subscription_id,
            )

            return subscription

        # ------------------------------------------------------
        # Update existing subscription
        # ------------------------------------------------------

        subscription.provider_subscription_id = (
            stripe_subscription_id
        )

        subscription.status = (
            local_status
        )

        subscription.auto_renew = (
            auto_renew
        )

        subscription.starts_at = (
            starts_at
        )

        subscription.expires_at = (
            expires_at
        )

        if cancelled_at is not None:
            subscription.cancelled_at = (
                cancelled_at
            )
        elif local_status == "active":
            subscription.cancelled_at = None

        self.subscriptions.update(
            subscription
        )

        logger.info(
            "Updated local subscription. "
            "subscription=%s status=%s",
            stripe_subscription_id,
            local_status,
        )

        return subscription

    # ==========================================================
    # Invoice Paid
    # ==========================================================

    def _invoice_paid(
        self,
        event: dict,
    ) -> None:
        """
        Handle successful recurring subscription payment.

        Stripe sends invoice.paid for recurring billing cycles.

        We synchronize the local subscription with Stripe.
        """

        data = self.webhook.data(
            event
        )

        stripe_subscription_id = (
            data.get("subscription")
        )

        if not stripe_subscription_id:
            logger.info(
                "Invoice paid without subscription ID."
            )
            return

        subscription = (
            self.subscriptions
            .get_by_provider_subscription_id(
                stripe_subscription_id
            )
        )

        if subscription is None:
            logger.warning(
                "Local subscription not found for "
                "invoice.paid: %s",
                stripe_subscription_id,
            )
            return

        # ------------------------------------------------------
        # Retrieve authoritative Stripe state
        # ------------------------------------------------------

        stripe_subscription = (
            self.webhook.subscription(
                stripe_subscription_id
            )
        )

        # ------------------------------------------------------
        # Update billing period
        # ------------------------------------------------------

        period_start = (
            stripe_subscription.get(
                "current_period_start"
            )
        )

        period_end = (
            stripe_subscription.get(
                "current_period_end"
            )
        )

        if period_start:
            subscription.starts_at = (
                datetime.fromtimestamp(
                    period_start,
                    tz=timezone.utc,
                )
            )

        if period_end:
            subscription.expires_at = (
                datetime.fromtimestamp(
                    period_end,
                    tz=timezone.utc,
                )
            )

        # ------------------------------------------------------
        # Update status
        # ------------------------------------------------------

        stripe_status = (
            stripe_subscription.get(
                "status"
            )
        )

        status_map = {
            "active": "active",
            "trialing": "active",
            "past_due": "past_due",
            "unpaid": "unpaid",
            "canceled": "cancelled",
        }

        subscription.status = status_map.get(
            stripe_status,
            "active",
        )

        subscription.auto_renew = not bool(
            stripe_subscription.get(
                "cancel_at_period_end",
                False,
            )
        )

        if stripe_subscription.get(
            "canceled_at"
        ):
            subscription.cancelled_at = (
                datetime.fromtimestamp(
                    stripe_subscription[
                        "canceled_at"
                    ],
                    tz=timezone.utc,
                )
            )

        self.subscriptions.update(
            subscription
        )

        logger.info(
            "Recurring invoice paid. "
            "Subscription renewed: %s",
            stripe_subscription_id,
        )

    # ==========================================================
    # Invoice Payment Failed
    # ==========================================================

    def _invoice_failed(
        self,
        event: dict,
    ) -> None:
        """
        Handle a failed recurring invoice.

        We do not immediately expire the subscription because
        Stripe can retry failed payments.
        """

        data = self.webhook.data(
            event
        )

        stripe_subscription_id = (
            data.get("subscription")
        )

        if not stripe_subscription_id:
            logger.warning(
                "Invoice payment failed without "
                "subscription ID."
            )
            return

        subscription = (
            self.subscriptions
            .get_by_provider_subscription_id(
                stripe_subscription_id
            )
        )

        if subscription is None:
            logger.warning(
                "Subscription not found for failed invoice: %s",
                stripe_subscription_id,
            )
            return

        subscription.status = "past_due"

        self.subscriptions.update(
            subscription
        )

        logger.warning(
            "Invoice payment failed. "
            "Subscription=%s",
            stripe_subscription_id,
        )

    # ==========================================================
    # Subscription Updated
    # ==========================================================

    def _subscription_updated(
        self,
        event: dict,
    ) -> None:
        """
        Synchronize a local subscription after Stripe updates it.
        """

        data = self.webhook.data(
            event
        )

        stripe_subscription_id = (
            data.get("id")
        )

        if not stripe_subscription_id:
            logger.warning(
                "Subscription update missing Stripe ID."
            )
            return

        subscription = (
            self.subscriptions
            .get_by_provider_subscription_id(
                stripe_subscription_id
            )
        )

        if subscription is None:
            logger.warning(
                "Local subscription not found for update: %s",
                stripe_subscription_id,
            )
            return

        # ------------------------------------------------------
        # Status
        # ------------------------------------------------------

        stripe_status = (
            data.get("status")
        )

        status_map = {
            "active": "active",
            "trialing": "active",
            "past_due": "past_due",
            "unpaid": "unpaid",
            "canceled": "cancelled",
            "incomplete": "incomplete",
            "incomplete_expired": "expired",
        }

        subscription.status = status_map.get(
            stripe_status,
            stripe_status or subscription.status,
        )

        # ------------------------------------------------------
        # Auto renewal
        # ------------------------------------------------------

        subscription.auto_renew = not bool(
            data.get(
                "cancel_at_period_end",
                False,
            )
        )

        # ------------------------------------------------------
        # Billing period
        # ------------------------------------------------------

        period_start = (
            data.get(
                "current_period_start"
            )
        )

        period_end = (
            data.get(
                "current_period_end"
            )
        )

        if period_start:
            subscription.starts_at = (
                datetime.fromtimestamp(
                    period_start,
                    tz=timezone.utc,
                )
            )

        if period_end:
            subscription.expires_at = (
                datetime.fromtimestamp(
                    period_end,
                    tz=timezone.utc,
                )
            )

        # ------------------------------------------------------
        # Cancellation
        # ------------------------------------------------------

        canceled_at = data.get(
            "canceled_at"
        )

        if canceled_at:
            subscription.cancelled_at = (
                datetime.fromtimestamp(
                    canceled_at,
                    tz=timezone.utc,
                )
            )

        elif subscription.status == "active":
            subscription.cancelled_at = None

        self.subscriptions.update(
            subscription
        )

        logger.info(
            "Subscription synchronized: %s",
            stripe_subscription_id,
        )

    # ==========================================================
    # Subscription Deleted
    # ==========================================================

    def _subscription_deleted(
        self,
        event: dict,
    ) -> None:
        """
        Handle permanent Stripe subscription cancellation.
        """

        data = self.webhook.data(
            event
        )

        stripe_subscription_id = (
            data.get("id")
        )

        if not stripe_subscription_id:
            logger.warning(
                "Subscription deletion missing Stripe ID."
            )
            return

        subscription = (
            self.subscriptions
            .get_by_provider_subscription_id(
                stripe_subscription_id
            )
        )

        if subscription is None:
            logger.warning(
                "Local subscription not found for deletion: %s",
                stripe_subscription_id,
            )
            return

        subscription.status = (
            "cancelled"
        )

        subscription.auto_renew = False

        canceled_at = data.get(
            "canceled_at"
        )

        if canceled_at:
            subscription.cancelled_at = (
                datetime.fromtimestamp(
                    canceled_at,
                    tz=timezone.utc,
                )
            )
        else:
            subscription.cancelled_at = (
                datetime.now(timezone.utc)
            )

        self.subscriptions.update(
            subscription
        )

        logger.info(
            "Subscription cancelled: %s",
            stripe_subscription_id,
        )