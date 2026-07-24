from sqlalchemy.orm import Session

from app.database.models.guest_session import GuestSession
from app.database.repositories.base_repository import (
    BaseRepository,
)


class GuestSessionRepository(
    BaseRepository[GuestSession],
):
    """
    Repository for GuestSession operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            GuestSession,
            db,
        )

    def get_by_session_token(
        self,
        session_token: str,
    ) -> GuestSession | None:

        return (
            self.db.query(
                GuestSession
            )
            .filter(
                GuestSession.session_token
                == session_token
            )
            .first()
        )

    def get_active(
        self,
    ) -> list[GuestSession]:

        return (
            self.db.query(
                GuestSession
            )
            .filter(
                GuestSession.active.is_(True)
            )
            .all()
        )

    def deactivate(
        self,
        session: GuestSession,
    ) -> GuestSession:

        session.active = False

        return self.update(session)