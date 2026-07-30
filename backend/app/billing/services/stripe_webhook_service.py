from datetime import datetime, timedelta

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


class StripeWebhookService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.orders = DatabaseOrderRepository(db)

        self.transactions = DatabaseTransactionRepository(db)

        self.subscriptions = (
            DatabaseSubscriptionRepository(db)
        )

    def payment_success(

        self,

        order_id: str,

        transaction_id: str,

        amount: float,

        currency: str,

    ):

        # -----------------------------
        # Order
        # -----------------------------

        order = self.orders.get(
            order_id
        )

        if order is None:

            raise ValueError(
                "Order not found."
            )

        order.status = "paid"

        self.orders.update(order)

        # -----------------------------
        # Transaction
        # -----------------------------

        transaction = PaymentTransaction(

            order_id=order.id,

            provider="stripe",

            provider_transaction_id=transaction_id,

            amount=amount,

            currency=currency,

            status="succeeded",

        )

        self.transactions.create(
            transaction
        )

        # -----------------------------
        # Subscription
        # -----------------------------

        subscription = Subscription(

            user_id=order.user_id,

            order_id=order.id,

            status="active",

            starts_at=datetime.utcnow(),

            expires_at=(
                datetime.utcnow()
                + timedelta(days=30)
            ),

        )

        self.subscriptions.create(
            subscription
        )

        return subscription




