from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest_session import GuestSession
from app.database.repositories.base_repository import BaseRepository


class GuestSessionRepository(BaseRepository[GuestSession]):
    """
    Repository for GuestSession database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(GuestSession, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_session_token(
        self,
        session_token: str,
    ) -> GuestSession | None:
        """
        Returns a guest session by its session token.
        """
        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.session_token == session_token,
            )
            .first()
        )

    def get_by_guest(
        self,
        guest_id: str,
    ) -> list[GuestSession]:
        """
        Returns all sessions belonging to a guest,
        ordered by newest first.
        """
        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.guest_id == guest_id,
            )
            .order_by(
                GuestSession.created_at.desc(),
            )
            .all()
        )

    def get_active(
        self,
    ) -> list[GuestSession]:
        """
        Returns all active guest sessions.
        """
        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.active.is_(True),
            )
            .all()
        )

    def session_token_exists(
        self,
        session_token: str,
    ) -> bool:
        """
        Returns True if the session token already exists.
        """
        return self.get_by_session_token(session_token) is not None

    def guest_has_active_session(
        self,
        guest_id: str,
    ) -> bool:
        """
        Returns True if the guest has at least one active session.
        """
        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.guest_id == guest_id,
                GuestSession.active.is_(True),
            )
            .first()
            is not None
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        session: GuestSession,
    ) -> GuestSession:
        """
        Activates a guest session.
        """
        session.active = True
        return self.update(session)

    def deactivate(
        self,
        session: GuestSession,
    ) -> GuestSession:
        """
        Deactivates a guest session.
        """
        session.active = False
        return self.update(session)