from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.guest.repository.guest_repository import GuestRepository
from app.referral.services.referral_service import ReferralService


class GuestService:
    """
    Business logic for anonymous guest access.

    Guest creation/session creation is also the entry point
    for referral attribution.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db
        self.repository = GuestRepository(db)
        self.referral_service = ReferralService(db)

    def create_or_get_session(
        self,
        browser_id: str,
        country: str = "IN",
        language: str = "en",
        user_agent: str | None = None,
        ip_address: str | None = None,
        referral_code: str | None = None,
    ) -> tuple[Guest, object]:
        """
        Create or retrieve a guest and create a new session.

        If referral_code is supplied for a new guest:

            1. Find the referrer by referral code.
            2. Create a pending referral.
            3. Create the referred guest session.

        Existing guests do not receive a second referral.
        """

        # ======================================================
        # 1. Find existing guest
        # ======================================================

        guest = self.repository.get_by_browser_id(
            browser_id,
        )

        is_new_guest = guest is None

        # ======================================================
        # 2. Create guest when necessary
        # ======================================================

        if is_new_guest:
            guest = self.repository.create_guest(
                browser_id=browser_id,
                country=country,
                language=language,
                user_agent=user_agent,
                ip_address=ip_address,
            )

        else:
            self.repository.touch_guest(guest)

        # ======================================================
        # 3. Referral attribution
        # ======================================================

        if is_new_guest and referral_code is not None:
            self._create_referral(
                referrer_code=referral_code,
                referred_guest=guest,
            )

        # ======================================================
        # 4. Create session
        # ======================================================

        session = self.repository.create_session(
            guest=guest,
            country=country,
            language=language,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        # ======================================================
        # 5. Commit everything atomically
        # ======================================================

        self.db.commit()

        return guest, session

    # ==========================================================
    # Referral
    # ==========================================================

    def _create_referral(
        self,
        referrer_code: str,
        referred_guest: Guest,
    ) -> None:
        """
        Attribute a newly created guest to a referrer.

        Raises:
            ValueError: If the referral code is invalid
                       or the referral is otherwise invalid.
        """

        # ------------------------------------------------------
        # Find referrer
        # ------------------------------------------------------

        referrer = (
            self.db.query(Guest)
            .filter(
                Guest.referral_code == referrer_code,
            )
            .first()
        )

        if referrer is None:
            raise ValueError(
                "Referral code not found."
            )

        # ------------------------------------------------------
        # Prevent self-referral
        # ------------------------------------------------------

        if referrer.id == referred_guest.id:
            raise ValueError(
                "A guest cannot refer themselves."
            )

        # ------------------------------------------------------
        # Create referral
        # ------------------------------------------------------

        self.referral_service.create_referral(
            referrer=referrer,
            referred=referred_guest,
        )