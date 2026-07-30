from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.payment_transaction import (
    PaymentTransaction,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class PaymentTransactionRepository(
    BaseRepository[PaymentTransaction],
):
    """
    Repository for PaymentTransaction database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            PaymentTransaction,
            db,
        )

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_order(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:
        """
        Returns all payment transactions for an order,
        ordered by newest first.
        """
        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.order_id == order_id
            )
            .order_by(
                PaymentTransaction.created_at.desc()
            )
            .all()
        )

    def get_by_provider_transaction(
        self,
        provider_transaction_id: str,
    ) -> PaymentTransaction | None:
        """
        Returns a transaction by the payment provider's
        transaction identifier.
        """
        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.provider_transaction_id
                == provider_transaction_id
            )
            .first()
        )

    def provider_transaction_exists(
        self,
        provider_transaction_id: str,
    ) -> bool:
        """
        Returns True if the provider transaction ID exists.
        """
        return (
            self.get_by_provider_transaction(
                provider_transaction_id
            )
            is not None
        )

    def get_successful(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:
        """
        Returns the successful transaction for an order.
        """
        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.order_id == order_id,
                PaymentTransaction.status == "success",
            )
            .first()
        )

    def get_failed(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:
        """
        Returns all failed transactions for an order.
        """
        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.order_id == order_id,
                PaymentTransaction.status == "failed",
            )
            .order_by(
                PaymentTransaction.created_at.desc()
            )
            .all()
        )

    def get_pending(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:
        """
        Returns all pending transactions for an order.
        """
        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.order_id == order_id,
                PaymentTransaction.status == "pending",
            )
            .order_by(
                PaymentTransaction.created_at.desc()
            )
            .all()
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def mark_successful(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Marks a transaction as successful.
        """
        transaction.status = "success"
        return self.update(transaction)

    def mark_failed(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Marks a transaction as failed.
        """
        transaction.status = "failed"
        return self.update(transaction)

    def mark_pending(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Marks a transaction as pending.
        """
        transaction.status = "pending"
        return self.update(transaction)