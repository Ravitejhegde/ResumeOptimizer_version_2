from sqlalchemy.orm import Session

from app.database.models.subscription import Subscription
from app.database.repositories.base_repository import (
    BaseRepository,
)


class SubscriptionRepository(
    BaseRepository[Subscription],
):
    """
    Repository for Subscription operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Subscription,
            db,
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> list[Subscription]:

        return (
            self.db.query(
                Subscription
            )
            .filter(
                Subscription.user_id == user_id
            )
            .order_by(
                Subscription.created_at.desc()
            )
            .all()
        )

    def get_active(
        self,
        user_id: str,
    ) -> Subscription | None:

        return (
            self.db.query(
                Subscription
            )
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .first()
        )

    def get_expired(
        self,
    ) -> list[Subscription]:

        return (
            self.db.query(
                Subscription
            )
            .filter(
                Subscription.status == "expired",
            )
            .all()
        )

    def cancel(
        self,
        subscription: Subscription,
    ) -> Subscription:

        subscription.status = "cancelled"

        return self.update(subscription)
    




