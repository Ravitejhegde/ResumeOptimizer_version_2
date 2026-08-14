from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.usage_event import UsageEvent
from app.database.repositories.base_repository import BaseRepository


class UsageRepository(BaseRepository[UsageEvent]):
    """
    Repository for UsageEvent database operations.

    All usage-event persistence and querying should go
    through this repository rather than being performed
    directly by application services.
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
        """Return all usage events for a user."""
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
        """Return all usage events for a guest session."""
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.guest_session_id
                == guest_session_id,
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
        """Return all events of a specific type."""
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

    # ==========================================================
    # Guest queries
    # ==========================================================

    def get_guest_events(
        self,
        guest_id: str,
        event_type: str | None = None,
    ) -> list[UsageEvent]:
        """
        Return events belonging to all sessions of a guest.

        Optionally filter by event type.
        """
        query = (
            self.db.query(UsageEvent)
            .join(
                UsageEvent.guest_session,
            )
            .filter(
                UsageEvent.guest_session.has(
                    guest_id=guest_id,
                )
            )
        )

        if event_type is not None:
            query = query.filter(
                UsageEvent.event_type == event_type,
            )

        return (
            query
            .order_by(
                UsageEvent.created_at.desc(),
            )
            .all()
        )

    def count_guest_events(
        self,
        guest_id: str,
        event_type: str | None = None,
    ) -> int:
        """
        Count events belonging to a guest.

        Optionally filter by event type.
        """
        query = (
            self.db.query(UsageEvent)
            .join(
                UsageEvent.guest_session,
            )
            .filter(
                UsageEvent.guest_session.has(
                    guest_id=guest_id,
                )
            )
        )

        if event_type is not None:
            query = query.filter(
                UsageEvent.event_type == event_type,
            )

        return query.count()

    # ==========================================================
    # Session queries
    # ==========================================================

    def count_guest_session_events(
        self,
        guest_session_id: str,
        event_type: str | None = None,
    ) -> int:
        """
        Count events belonging to one guest session.

        Optionally filter by event type.
        """
        query = (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.guest_session_id
                == guest_session_id,
            )
        )

        if event_type is not None:
            query = query.filter(
                UsageEvent.event_type == event_type,
            )

        return query.count()

    def guest_session_has_event(
        self,
        guest_session_id: str,
        event_type: str,
    ) -> bool:
        """
        Return True if the session already contains
        an event of the specified type.
        """
        return (
            self.count_guest_session_events(
                guest_session_id=guest_session_id,
                event_type=event_type,
            )
            > 0
        )

    # ==========================================================
    # User counts
    # ==========================================================

    def count_by_user(
        self,
        user_id: str,
    ) -> int:
        """Return total usage events for a user."""
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
        """Return total usage events for a guest session."""
        return (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.guest_session_id
                == guest_session_id,
            )
            .count()
        )

    # ==========================================================
    # Existence helpers
    # ==========================================================

    def user_has_events(
        self,
        user_id: str,
    ) -> bool:
        """Return True if the user has usage events."""
        return self.count_by_user(user_id) > 0

    def guest_session_has_events(
        self,
        guest_session_id: str,
    ) -> bool:
        """Return True if the session has usage events."""
        return (
            self.count_by_guest_session(
                guest_session_id
            )
            > 0
        )