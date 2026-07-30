from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.order import Order


class DatabaseOrderRepository:
    """
    Billing order database repository.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db


    def create(
        self,
        order: Order,
    ) -> Order:

        self.db.add(order)

        self.db.flush()

        return order


    def update(
        self,
        order: Order,
    ) -> Order:

        self.db.add(order)

        self.db.flush()

        return order


    def get(
        self,
        order_id: str,
    ) -> Order | None:

        return (
            self.db.query(Order)
            .filter(
                Order.id == order_id
            )
            .first()
        )


    def get_by_provider_order_id(
        self,
        provider_order_id: str,
    ) -> Order | None:

        return (
            self.db.query(Order)
            .filter(
                Order.provider_order_id == provider_order_id
            )
            .first()
        )