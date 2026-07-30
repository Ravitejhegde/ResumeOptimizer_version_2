from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.usage_event import UsageEvent
from app.database.repositories.base_repository import BaseRepository


class UsageRepository(BaseRepository[UsageEvent]):
    """
    Repository for UsageEvent database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(UsageEvent, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_user(
        self,
        user_id: str,
    ) -> list[UsageEvent]:
        """
        Returns all usage events for a user,
        ordered by newest first.
        """
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.user_id == user_id,
            )
            .order_by(
                UsageEvent.created_at.desc(),
            )
            .all()
        )

    def get_by_guest_session(
        self,
        guest_session_id: str,
    ) -> list[UsageEvent]:
        """
        Returns all usage events for a guest session,
        ordered by newest first.
        """
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.guest_session_id == guest_session_id,
            )
            .order_by(
                UsageEvent.created_at.desc(),
            )
            .all()
        )

    def get_by_event_type(
        self,
        event_type: str,
    ) -> list[UsageEvent]:
        """
        Returns all events of the specified type.
        """
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.event_type == event_type,
            )
            .order_by(
                UsageEvent.created_at.desc(),
            )
            .all()
        )

    def count_by_user(
        self,
        user_id: str,
    ) -> int:
        """
        Returns the total number of usage events
        for a user.
        """
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.user_id == user_id,
            )
            .count()
        )

    def count_by_guest_session(
        self,
        guest_session_id: str,
    ) -> int:
        """
        Returns the total number of usage events
        for a guest session.
        """
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.guest_session_id == guest_session_id,
            )
            .count()
        )

    def user_has_events(
        self,
        user_id: str,
    ) -> bool:
        """
        Returns True if the user has recorded usage events.
        """
        return self.count_by_user(user_id) > 0

    def guest_session_has_events(
        self,
        guest_session_id: str,
    ) -> bool:
        """
        Returns True if the guest session has recorded usage events.
        """
        return self.count_by_guest_session(guest_session_id) > 0