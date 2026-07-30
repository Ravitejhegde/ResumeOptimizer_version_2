from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.billing.providers.stripe.webhook import (
    StripeWebhook,
)

from app.database.models.payment_transaction import (
    PaymentTransaction,
)

from app.database.models.subscription import (
    Subscription,
)

from app.database.repositories.order_repository import (
    OrderRepository,
)

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
    Handles payment provider webhook events.

    Flow:

    Stripe Event
        ↓
    Verify
        ↓
    Duplicate Check
        ↓
    Update Database
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.webhook = StripeWebhook()

        self.orders = OrderRepository(
            db
        )

        self.transactions = (
            PaymentTransactionRepository(db)
        )

        self.subscriptions = (
            SubscriptionRepository(db)
        )

        self.events = (
            WebhookEventRepository(db)
        )

    # ==========================================================
    # Main Handler
    # ==========================================================

    def process(
        self,
        payload: bytes,
        signature: str,
    ) -> dict:

        event = self.webhook.verify(
            payload,
            signature,
        )

        event_id = event["id"]
        event_type = event["type"]

        # ----------------------------------
        # Duplicate protection
        # ----------------------------------

        if self.events.exists(
            "stripe",
            event_id,
        ):
            return {
                "duplicate": True,
                "event_id": event_id,
            }

        self.events.create(
            provider="stripe",
            event_id=event_id,
            event_type=event_type,
        )

        # ----------------------------------
        # Event routing
        # ----------------------------------

        if self.webhook.is_checkout_completed(
            event
        ):
            self._checkout_completed(event)

        elif self.webhook.is_invoice_paid(
            event
        ):
            self._invoice_paid(event)

        elif self.webhook.is_invoice_failed(
            event
        ):
            self._invoice_failed(event)

        elif self.webhook.is_subscription_updated(
            event
        ):
            self._subscription_updated(event)

        elif self.webhook.is_subscription_deleted(
            event
        ):
            self._subscription_deleted(event)

        logger.info(
            "Webhook processed: %s",
            event_type,
        )

        return {
            "processed": True,
            "event": event_type,
            "event_id": event_id,
        }

    # ==========================================================
    # Checkout Completed
    # ==========================================================

    def _checkout_completed(
        self,
        event: dict,
    ) -> None:

        data = self.webhook.data(
            event
        )

        order = self.orders.get(
            data["client_reference_id"]
        )

        if order is None:
            return

        order.status = "completed"

        self.orders.update(
            order
        )

        transaction = PaymentTransaction(
            order_id=order.id,
            provider="stripe",
            provider_transaction_id=data.get(
                "payment_intent"
            ),
            amount=order.amount,
            currency=order.currency,
            status="success",
        )

        self.transactions.create(
            transaction
        )

        subscription = Subscription(
            user_id=order.user_id,
            order_id=order.id,
            status="active",
            starts_at=datetime.now(
                timezone.utc
            ),
            expires_at=datetime.now(
                timezone.utc
            ),
        )

        self.subscriptions.create(
            subscription
        )

    # ==========================================================
    # Invoice Paid
    # ==========================================================

    def _invoice_paid(
        self,
        event: dict,
    ) -> None:

        logger.info(
            "Invoice paid"
        )

    # ==========================================================
    # Invoice Failed
    # ==========================================================

    def _invoice_failed(
        self,
        event: dict,
    ) -> None:

        logger.warning(
            "Invoice payment failed"
        )

    # ==========================================================
    # Subscription Updated
    # ==========================================================

    def _subscription_updated(
        self,
        event: dict,
    ) -> None:

        logger.info(
            "Subscription updated"
        )

    # ==========================================================
    # Subscription Deleted
    # ==========================================================

    def _subscription_deleted(
        self,
        event: dict,
    ) -> None:

        logger.info(
            "Subscription deleted"
        )