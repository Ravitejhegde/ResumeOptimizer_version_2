from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.order import Order
from app.database.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Order, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_user(
        self,
        user_id: str,
    ) -> list[Order]:
        """
        Returns all orders for a user,
        ordered by newest first.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
            )
            .order_by(
                Order.created_at.desc(),
            )
            .all()
        )

    def get_latest(
        self,
        user_id: str,
    ) -> Order | None:
        """
        Returns the latest order for a user.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
            )
            .order_by(
                Order.created_at.desc(),
            )
            .first()
        )

    def get_pending(
        self,
        user_id: str,
    ) -> list[Order]:
        """
        Returns all pending orders for a user.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
                Order.status == "pending",
            )
            .order_by(
                Order.created_at.desc(),
            )
            .all()
        )

    def get_completed(
        self,
        user_id: str,
    ) -> list[Order]:
        """
        Returns all completed orders for a user.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
                Order.status == "completed",
            )
            .order_by(
                Order.created_at.desc(),
            )
            .all()
        )

    def get_failed(
        self,
        user_id: str,
    ) -> list[Order]:
        """
        Returns all failed orders for a user.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
                Order.status == "failed",
            )
            .order_by(
                Order.created_at.desc(),
            )
            .all()
        )

    def user_has_orders(
        self,
        user_id: str,
    ) -> bool:
        """
        Returns True if the user has placed any orders.
        """
        return (
            self.db.query(Order)
            .filter(
                Order.user_id == user_id,
            )
            .first()
            is not None
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def mark_completed(
        self,
        order: Order,
    ) -> Order:
        """
        Marks an order as completed.
        """
        order.status = "completed"
        return self.update(order)

    def mark_failed(
        self,
        order: Order,
    ) -> Order:
        """
        Marks an order as failed.
        """
        order.status = "failed"
        return self.update(order)