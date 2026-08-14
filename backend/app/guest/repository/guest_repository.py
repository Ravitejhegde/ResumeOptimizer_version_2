from __future__ import annotations

from datetime import datetime, timezone
from secrets import token_urlsafe

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession


class GuestRepository:
    """
    Database access for anonymous guests and guest sessions.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_browser_id(
        self,
        browser_id: str,
    ) -> Guest | None:
        return (
            self.db.query(Guest)
            .filter(
                Guest.browser_id == browser_id,
            )
            .first()
        )

    def create_guest(
        self,
        browser_id: str,
        country: str = "IN",
        language: str = "en",
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> Guest:

        now = datetime.now(timezone.utc)

        guest = Guest(
            browser_id=browser_id,
            country=country.upper(),
            language=language,
            user_agent=user_agent,
            ip_address=ip_address,
            created_at=now,
            last_seen=now,
        )

        self.db.add(guest)
        self.db.flush()

        return guest

    def create_session(
        self,
        guest: Guest,
        country: str | None = None,
        language: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> GuestSession:

        now = datetime.now(timezone.utc)

        session = GuestSession(
            guest_id=guest.id,
            session_token=token_urlsafe(48),
            country=(
                country.upper()
                if country
                else guest.country
            ),
            language=(
                language
                if language
                else guest.language
            ),
            user_agent=(
                user_agent
                if user_agent is not None
                else guest.user_agent
            ),
            ip_address=(
                ip_address
                if ip_address is not None
                else guest.ip_address
            ),
            active=True,
            created_at=now,
            last_activity_at=now,
        )

        self.db.add(session)
        self.db.flush()

        return session

    def get_session(
        self,
        session_token: str,
    ) -> GuestSession | None:

        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.session_token == session_token,
                GuestSession.active.is_(True),
            )
            .first()
        )

    def get_session_with_guest(
        self,
        session_token: str,
    ) -> GuestSession | None:
        """
        Return an active guest session by token.

        The returned session belongs to a Guest through
        GuestSession.guest.
        """

        return (
            self.db.query(GuestSession)
            .filter(
                GuestSession.session_token == session_token,
                GuestSession.active.is_(True),
            )
            .first()
        )   

    def touch_guest(
        self,
        guest: Guest,
    ) -> None:

        guest.last_seen = datetime.now(timezone.utc)

    def touch_session(
        self,
        session: GuestSession,
    ) -> None:

        session.last_activity_at = datetime.now(timezone.utc)