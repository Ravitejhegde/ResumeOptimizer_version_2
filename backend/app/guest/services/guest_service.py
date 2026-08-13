from __future__ import annotations

from sqlalchemy.orm import Session

from app.guest.repository.guest_repository import GuestRepository


class GuestService:
    """
    Business logic for anonymous guest access.
    """

    def __init__(self, db: Session) -> None:
        self.repository = GuestRepository(db)
        self.db = db

    def create_or_get_session(
        self,
        browser_id: str,
        country: str = "IN",
        language: str = "en",
        user_agent: str | None = None,
        ip_address: str | None = None,
    ):

        guest = self.repository.get_by_browser_id(
            browser_id,
        )

        if guest is None:
            guest = self.repository.create_guest(
                browser_id=browser_id,
                country=country,
                language=language,
                user_agent=user_agent,
                ip_address=ip_address,
            )
        else:
            self.repository.touch_guest(guest)

        session = self.repository.create_session(
            guest=guest,
            country=country,
            language=language,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        self.db.commit()

        return guest, session