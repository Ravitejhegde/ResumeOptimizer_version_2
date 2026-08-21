from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.subscription import Subscription
from app.database.repositories.base_repository import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    """
    Repository for Subscription database operations.

    Responsibilities:
    - Query subscriptions.
    - Find subscriptions by user, order, or provider ID.
    - Manage subscription state.

    Business logic should remain in services.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            Subscription,
            db,
        )

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

    def get_by_provider_subscription_id(
        self,
        provider_subscription_id: str,
    ) -> Subscription | None:
        """
        Returns a subscription by its payment-provider
        subscription identifier.

        Example:
            Stripe subscription ID:
            sub_123456789
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.provider_subscription_id
                == provider_subscription_id,
            )
            .first()
        )

    def get_by_order(
        self,
        order_id: str,
    ) -> Subscription | None:
        """
        Returns the subscription associated with an order.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.order_id == order_id,
            )
            .first()
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

        return self.update(
            subscription
        )

    def cancel(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Cancels a subscription.
        """
        subscription.status = "cancelled"

        return self.update(
            subscription
        )

    def expire(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Marks a subscription as expired.
        """
        subscription.status = "expired"

        return self.update(
            subscription
        )