from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.subscription import Subscription
from app.database.repositories.base_repository import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    """
    Repository for Subscription database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Subscription, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_user(
        self,
        user_id: str,
    ) -> list[Subscription]:
        """
        Returns all subscriptions for a user,
        ordered by newest first.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
            )
            .order_by(
                Subscription.created_at.desc(),
            )
            .all()
        )

    def get_latest(
        self,
        user_id: str,
    ) -> Subscription | None:
        """
        Returns the latest subscription for a user.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
            )
            .order_by(
                Subscription.created_at.desc(),
            )
            .first()
        )

    def get_active(
        self,
        user_id: str,
    ) -> Subscription | None:
        """
        Returns the user's active subscription.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .first()
        )

    def get_expired(
        self,
    ) -> list[Subscription]:
        """
        Returns all expired subscriptions.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.status == "expired",
            )
            .all()
        )

    def user_has_active_subscription(
        self,
        user_id: str,
    ) -> bool:
        """
        Returns True if the user has an active subscription.
        """
        return self.get_active(user_id) is not None

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Activates a subscription.
        """
        subscription.status = "active"
        return self.update(subscription)

    def cancel(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Cancels a subscription.
        """
        subscription.status = "cancelled"
        return self.update(subscription)