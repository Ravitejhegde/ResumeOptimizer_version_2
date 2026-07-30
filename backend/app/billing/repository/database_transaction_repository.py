from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.payment_transaction import (
    PaymentTransaction,
)


class DatabaseTransactionRepository:
    """
    Payment transaction database repository.

    Responsibilities:
        - Create transactions
        - Update transactions
        - Retrieve transactions

    Does not:
        - Handle Stripe logic
        - Handle webhook processing
        - Handle payment rules
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
        Create payment transaction.
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
        Update payment transaction.
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
        Get transaction by id.
        """

        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.id == transaction_id
            )
            .first()
        )


    def get_by_provider_transaction_id(
        self,
        provider_transaction_id: str,
    ) -> PaymentTransaction | None:
        """
        Find transaction using Stripe payment id.
        """

        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.provider_transaction_id
                == provider_transaction_id
            )
            .first()
        )


    def get_by_order_id(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:
        """
        Find transaction by order.
        """

        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.order_id == order_id
            )
            .first()
        )