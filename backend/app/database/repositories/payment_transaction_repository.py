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
    Repository for PaymentTransaction operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            PaymentTransaction,
            db,
        )

    def get_by_order(
        self,
        order_id: str,
    ) -> list[PaymentTransaction]:

        return (
            self.db.query(
                PaymentTransaction
            )
            .filter(
                PaymentTransaction.order_id
                == order_id
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

    def get_successful(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:

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




