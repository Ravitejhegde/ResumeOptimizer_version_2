from sqlalchemy.orm import Session

from app.database.models.order import Order

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)


class CheckoutOrchestrator:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.orders = DatabaseOrderRepository(
            db
        )

    def create_order(

        self,

        user_id: str,

        pricing_id: str,

        amount: float,

        currency: str,

    ) -> Order:

        order = Order(

            user_id=user_id,

            pricing_id=pricing_id,

            amount=amount,

            currency=currency,

            status="pending",

        )

        return self.orders.create(
            order
        )




