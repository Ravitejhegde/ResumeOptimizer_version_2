from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)
from app.billing.repository.database_subscription_repository import (
    DatabaseSubscriptionRepository,
)
from app.billing.repository.database_transaction_repository import (
    DatabaseTransactionRepository,
)
from app.database.models.payment_transaction import PaymentTransaction
from app.database.models.subscription import Subscription


logger = logging.getLogger(__name__)


class StripeWebhookService:
    """
    Handles Stripe webhook business logic.

    Responsibilities:
        - Process successful checkout events.
        - Update local orders.
        - Create payment transactions.
        - Create or update subscriptions.
        - Maintain payment idempotency.

    Does not:
        - Verify Stripe signatures.
        - Handle HTTP requests.
        - Communicate directly with Stripe.
    """

    SUBSCRIPTION_DURATION_DAYS = 30

    def __init__(self, db: Session) -> None:
        self.db = db

        self.orders = DatabaseOrderRepository(db)

        self.transactions = DatabaseTransactionRepository(db)

        self.subscriptions = DatabaseSubscriptionRepository(db)

    # ==========================================================
    # Payment Success
    # ==========================================================

    def payment_success(
        self,
        *,
        order_id: str,
        transaction_id: str,
        amount: Decimal | float | int,
        currency: str,
        provider_subscription_id: str | None = None,
        provider_order_id: str | None = None,
    ) -> Subscription:
        """
        Process a successful Stripe payment.

        This method is intentionally idempotent.

        Reprocessing the same provider transaction must NOT:
            - create another payment transaction
            - create another subscription
            - extend the subscription twice
        """

        # ------------------------------------------------------
        # Find order
        # ------------------------------------------------------

        order = self.orders.get(order_id)

        if order is None:
            raise ValueError("Order not found.")

        # ------------------------------------------------------
        # Validate provider
        # ------------------------------------------------------

        if order.provider != "stripe":
            raise ValueError(
                "Order payment provider does not match Stripe."
            )

        # ------------------------------------------------------
        # Idempotency
        # ------------------------------------------------------

        existing_transaction = (
            self.transactions.get_by_provider_transaction_id(
                transaction_id
            )
        )

        if existing_transaction is not None:

            existing_subscription = (
                self.subscriptions.get_by_user(
                    order.user_id
                )
            )

            if existing_subscription is None:
                raise ValueError(
                    "Payment transaction already exists "
                    "but subscription was not found."
                )

            logger.info(
                "Ignoring duplicate Stripe payment transaction %s",
                transaction_id,
            )

            return existing_subscription

        # ------------------------------------------------------
        # Validate amount
        # ------------------------------------------------------

        expected_amount = Decimal(str(order.amount))
        received_amount = Decimal(str(amount))

        if expected_amount != received_amount:
            raise ValueError(
                "Stripe payment amount does not match "
                "the order amount."
            )

        # ------------------------------------------------------
        # Validate currency
        # ------------------------------------------------------

        normalized_currency = currency.strip().upper()

        if order.currency.upper() != normalized_currency:
            raise ValueError(
                "Stripe payment currency does not match "
                "the order currency."
            )

        # ------------------------------------------------------
        # Prevent already-completed order from being processed
        # with a different transaction.
        # ------------------------------------------------------

        if order.status == "paid":
            raise ValueError(
                "Order is already marked as paid with "
                "a different payment transaction."
            )

        # ------------------------------------------------------
        # Update order
        # ------------------------------------------------------

        order.status = "paid"

        if provider_order_id:
            order.provider_order_id = provider_order_id

        self.orders.update(order)

        # ------------------------------------------------------
        # Create payment transaction
        # ------------------------------------------------------

        transaction = PaymentTransaction(
            order_id=order.id,
            provider="stripe",
            provider_transaction_id=transaction_id,
            amount=received_amount,
            currency=normalized_currency,
            status="paid",
        )

        self.transactions.create(transaction)

        # ------------------------------------------------------
        # Find existing subscription
        # ------------------------------------------------------

        existing_subscription = (
            self.subscriptions.get_by_user(
                order.user_id
            )
        )

        now = datetime.now(timezone.utc)

        # ------------------------------------------------------
        # Extend existing subscription
        # ------------------------------------------------------

        if existing_subscription is not None:

            if (
                existing_subscription.is_active
                and existing_subscription.expires_at > now
            ):
                starts_at = existing_subscription.expires_at
            else:
                starts_at = now

            existing_subscription.starts_at = starts_at

            existing_subscription.expires_at = (
                starts_at
                + timedelta(
                    days=self.SUBSCRIPTION_DURATION_DAYS
                )
            )

            existing_subscription.status = "active"
            existing_subscription.auto_renew = True
            existing_subscription.cancelled_at = None

            if provider_subscription_id:
                existing_subscription.provider_subscription_id = (
                    provider_subscription_id
                )

            self.subscriptions.update(
                existing_subscription
            )

            self.db.commit()

            logger.info(
                "Existing subscription extended for user %s",
                order.user_id,
            )

            return existing_subscription

        # ------------------------------------------------------
        # Create subscription
        # ------------------------------------------------------

        subscription = Subscription(
            user_id=order.user_id,
            order_id=order.id,
            status="active",
            auto_renew=True,
            starts_at=now,
            expires_at=(
                now
                + timedelta(
                    days=self.SUBSCRIPTION_DURATION_DAYS
                )
            ),
            provider_subscription_id=(
                provider_subscription_id
            ),
        )

        self.subscriptions.create(subscription)

        # ------------------------------------------------------
        # Commit transaction
        # ------------------------------------------------------

        self.db.commit()

        logger.info(
            "Stripe payment successfully processed. "
            "order=%s transaction=%s user=%s",
            order.id,
            transaction_id,
            order.user_id,
        )

        return subscription