from sqlalchemy.orm import Session

from app.database.models.order import Order
from app.database.models.payment_transaction import (
    PaymentTransaction,
)
from app.database.repositories.order_repository import (
    OrderRepository,
)
from app.database.repositories.payment_transaction_repository import (
    PaymentTransactionRepository,
)


class PaymentService:
    """
    Business logic for orders and payments.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.orders = OrderRepository(db)
        self.transactions = PaymentTransactionRepository(
            db
        )

    # --------------------------------------------------
    # Orders
    # --------------------------------------------------

    def create_order(
        self,
        order: Order,
    ) -> Order:

        return self.orders.create(order)

    def get_order(
        self,
        order_id: str,
    ) -> Order | None:

        return self.orders.get(order_id)

    def get_user_orders(
        self,
        user_id: str,
    ) -> list[Order]:

        return self.orders.get_by_user(user_id)

    def get_pending_orders(
        self,
        user_id: str,
    ) -> list[Order]:

        return self.orders.get_pending(user_id)

    def get_completed_orders(
        self,
        user_id: str,
    ) -> list[Order]:

        return self.orders.get_completed(user_id)

    # --------------------------------------------------
    # Payment Transactions
    # --------------------------------------------------

    def create_transaction(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:

        return self.transactions.create(
            transaction
        )

    def get_transaction(
        self,
        transaction_id: str,
    ) -> PaymentTransaction | None:

        return self.transactions.get(
            transaction_id
        )

    def get_order_transactions(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:

        return self.transactions.get_by_order(
            order_id
        )

    def get_successful_transaction(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:

        return self.transactions.get_successful(
            order_id
        )

    def get_failed_transactions(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:

        return self.transactions.get_failed(
            order_id
        )




