from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.usage_event import UsageEvent
from app.database.repositories.base_repository import (
    BaseRepository,
)


class UsageEventRepository(
    BaseRepository[UsageEvent],
):
    """
    Repository for UsageEvent operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            UsageEvent,
            db,
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> list[UsageEvent]:

        return (
            self.db.query(
                UsageEvent
            )
            .filter(
                UsageEvent.user_id == user_id
            )
            .order_by(
                UsageEvent.created_at.desc()
            )
            .all()
        )

    def get_by_guest(
        self,
        guest_session_id: str,
    ) -> list[UsageEvent]:

        return (
            self.db.query(
                UsageEvent
            )
            .filter(
                UsageEvent.guest_session_id
                == guest_session_id
            )
            .order_by(
                UsageEvent.created_at.desc()
            )
            .all()
        )

    def get_by_event_type(
        self,
        event_type: str,
    ) -> list[UsageEvent]:

        return (
            self.db.query(
                UsageEvent
            )
            .filter(
                UsageEvent.event_type
                == event_type
            )
            .order_by(
                UsageEvent.created_at.desc()
            )
            .all()
        )

    def get_between(
        self,
        start: datetime,
        end: datetime,
    ) -> list[UsageEvent]:

        return (
            self.db.query(
                UsageEvent
            )
            .filter(
                UsageEvent.created_at >= start,
                UsageEvent.created_at <= end,
            )
            .order_by(
                UsageEvent.created_at.desc()
            )
            .all()
        )




