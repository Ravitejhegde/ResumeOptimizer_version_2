from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.subscription import (
    Subscription,
)


class DatabaseSubscriptionRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def create(
        self,
        subscription: Subscription,
    ) -> Subscription:

        self.db.add(subscription)

        self.db.commit()

        self.db.refresh(subscription)

        return subscription

    def update(
        self,
        subscription: Subscription,
    ) -> Subscription:

        self.db.commit()

        self.db.refresh(subscription)

        return subscription

    def get(
        self,
        subscription_id: str,
    ) -> Subscription | None:

        return (

            self.db.query(
                Subscription
            )

            .filter(

                Subscription.id
                == subscription_id

            )

            .first()

        )

    def by_user(
        self,
        user_id: str,
    ) -> list[Subscription]:

        return (

            self.db.query(
                Subscription
            )

            .filter(

                Subscription.user_id
                == user_id

            )

            .order_by(

                Subscription.created_at.desc()

            )

            .all()

        )

    def active(
        self,
        user_id: str,
    ) -> Subscription | None:

        return (

            self.db.query(
                Subscription
            )

            .filter(

                Subscription.user_id
                == user_id,

                Subscription.status
                == "active",

                Subscription.expires_at
                > datetime.utcnow(),

            )

            .first()

        )

    def expired(
        self,
    ) -> list[Subscription]:

        return (

            self.db.query(
                Subscription
            )

            .filter(

                Subscription.expires_at
                <= datetime.utcnow(),

                Subscription.status
                == "active",

            )

            .all()

        )

    def cancel(
        self,
        subscription: Subscription,
    ) -> Subscription:

        subscription.status = "cancelled"

        subscription.cancelled_at = (
            datetime.utcnow()
        )

        self.db.commit()

        self.db.refresh(
            subscription
        )

        return subscription

    def delete(
        self,
        subscription: Subscription,
    ) -> None:

        self.db.delete(
            subscription
        )

        self.db.commit()




