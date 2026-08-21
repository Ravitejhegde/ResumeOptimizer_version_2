from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.subscription import Subscription


class DatabaseSubscriptionRepository:
    """
    Billing subscription database repository.

    Responsibilities:
        - Create subscriptions
        - Update subscriptions
        - Retrieve subscriptions

    Does not:
        - Handle Stripe logic
        - Handle billing business rules
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    def create(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Add a subscription to the current database transaction.

        The transaction is not committed here.
        """
        self.db.add(subscription)
        self.db.flush()

        return subscription

    # ==========================================================
    # Update
    # ==========================================================

    def update(
        self,
        subscription: Subscription,
    ) -> Subscription:
        """
        Update a subscription within the current transaction.

        The transaction is not committed here.
        """
        self.db.add(subscription)
        self.db.flush()

        return subscription

    # ==========================================================
    # Queries
    # ==========================================================

    def get(
        self,
        subscription_id: str,
    ) -> Subscription | None:
        """
        Return a subscription by its primary key.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.id == subscription_id,
            )
            .first()
        )

    def get_by_provider_subscription_id(
        self,
        provider_subscription_id: str,
    ) -> Subscription | None:
        """
        Return a subscription by its payment-provider subscription ID.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.provider_subscription_id
                == provider_subscription_id,
            )
            .first()
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> Subscription | None:
        """
        Return a subscription belonging to a user.
        """
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
            )
            .first()
        )