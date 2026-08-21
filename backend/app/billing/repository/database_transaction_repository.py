from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.payment_transaction import (
    PaymentTransaction,
)
from app.database.models.payment_transaction import (
    PaymentTransaction,
)

class DatabaseTransactionRepository:
    """
    Billing payment transaction database repository.

    Responsibilities:
        - Create payment transactions
        - Update payment transactions
        - Retrieve payment transactions

    Does not:
        - Handle Stripe logic
        - Handle webhook processing
        - Handle payment business rules
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    def create(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Add a payment transaction to the current transaction.

        The database transaction is not committed here.
        """
        self.db.add(transaction)
        self.db.flush()

        return transaction

    # ==========================================================
    # Update
    # ==========================================================

    def update(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Update a payment transaction within the current transaction.

        The database transaction is not committed here.
        """
        self.db.add(transaction)
        self.db.flush()

        return transaction

    # ==========================================================
    # Queries
    # ==========================================================

    def get(
        self,
        transaction_id: str,
    ) -> PaymentTransaction | None:
        """
        Return a payment transaction by its primary key.
        """
        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.id == transaction_id,
            )
            .first()
        )

    def get_by_provider_transaction_id(
        self,
        provider_transaction_id: str,
    ) -> PaymentTransaction | None:
        """
        Return a payment transaction by its provider transaction ID.
        """
        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.provider_transaction_id
                == provider_transaction_id,
            )
            .first()
        )

    def get_by_order_id(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:
        """
        Return a payment transaction belonging to an order.
        """
        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.order_id == order_id,
            )
            .first()
        )