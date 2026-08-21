from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.order import Order
from app.database.repositories.order_repository import (
    OrderRepository,
)


class DatabaseOrderRepository:
    """
    Compatibility repository for billing order operations.

    This class preserves the existing billing-layer API while
    delegating database operations to the canonical OrderRepository.

    Architecture:

        Billing Services
              ↓
        DatabaseOrderRepository
              ↓
        OrderRepository
              ↓
        BaseRepository
              ↓
        Database
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self._repository = OrderRepository(db)

    # ==========================================================
    # Create
    # ==========================================================

    def create(
        self,
        order: Order,
    ) -> Order:
        """
        Create an order within the current database transaction.

        Does not commit.
        """
        return self._repository.create_flush(order)

    # ==========================================================
    # Update
    # ==========================================================

    def update(
        self,
        order: Order,
    ) -> Order:
        """
        Update an order within the current database transaction.

        Does not commit.
        """
        return self._repository.update_flush(order)

    # ==========================================================
    # Queries
    # ==========================================================

    def get(
        self,
        order_id: str,
    ) -> Order | None:
        """
        Return an order by its ID.
        """
        return self._repository.get(order_id)

    def get_by_provider_order_id(
        self,
        provider_order_id: str,
    ) -> Order | None:
        """
        Return an order by the payment provider's order/session ID.
        """
        return (
            self._repository.db.query(Order)
            .filter(
                Order.provider_order_id
                == provider_order_id
            )
            .first()
        )