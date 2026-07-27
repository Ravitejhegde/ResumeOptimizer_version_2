from sqlalchemy.orm import Session

from app.database.models.order import Order
from app.database.repositories.base_repository import (
    BaseRepository,
)


class OrderRepository(
    BaseRepository[Order],
):
    """
    Repository for Order operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Order,
            db,
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> list[Order]:

        return (
            self.db.query(
                Order
            )
            .filter(
                Order.user_id == user_id
            )
            .order_by(
                Order.created_at.desc()
            )
            .all()
        )

    def get_pending(
        self,
        user_id: str,
    ) -> list[Order]:

        return (
            self.db.query(
                Order
            )
            .filter(
                Order.user_id == user_id,
                Order.status == "pending",
            )
            .order_by(
                Order.created_at.desc()
            )
            .all()
        )

    def get_completed(
        self,
        user_id: str,
    ) -> list[Order]:

        return (
            self.db.query(
                Order
            )
            .filter(
                Order.user_id == user_id,
                Order.status == "completed",
            )
            .order_by(
                Order.created_at.desc()
            )
            .all()
        )




