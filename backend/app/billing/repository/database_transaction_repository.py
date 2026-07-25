from sqlalchemy.orm import Session

from app.database.models.payment_transaction import (
    PaymentTransaction,
)


class DatabaseTransactionRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def create(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:

        self.db.add(
            transaction
        )

        self.db.commit()

        self.db.refresh(
            transaction
        )

        return transaction

    def update(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:

        self.db.commit()

        self.db.refresh(
            transaction
        )

        return transaction

    def get(
        self,
        transaction_id: str,
    ) -> PaymentTransaction | None:

        return (

            self.db.query(
                PaymentTransaction
            )

            .filter(

                PaymentTransaction.id
                == transaction_id

            )

            .first()

        )

    def by_provider_transaction_id(
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

    def by_order(
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

    def successful(
        self,
        order_id: str,
    ) -> PaymentTransaction | None:

        return (

            self.db.query(
                PaymentTransaction
            )

            .filter(

                PaymentTransaction.order_id
                == order_id,

                PaymentTransaction.status
                == "succeeded",

            )

            .first()

        )

    def delete(
        self,
        transaction: PaymentTransaction,
    ) -> None:

        self.db.delete(
            transaction
        )

        self.db.commit()