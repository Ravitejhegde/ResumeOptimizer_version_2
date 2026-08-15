from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.referral import Referral
from app.referral.repository.referral_repository import ReferralRepository


class ReferralService:
    """
    Business logic for guest referrals.

    A referral starts as "pending".

    It becomes "completed" only when the application explicitly
    qualifies the referred guest.

    Rewards are granted separately after qualification.
    """

    PENDING = "pending"
    COMPLETED = "completed"

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db
        self.repository = ReferralRepository(db)

    # ==========================================================
    # Create Referral
    # ==========================================================

    def create_referral(
        self,
        referrer: Guest,
        referred: Guest,
    ) -> Referral:
        """
        Create a referral relationship between two guests.

        Rules:

        1. A guest cannot refer themselves.
        2. A referred guest can have only one referrer.
        3. The same referral relationship cannot be created twice.
        4. New referrals start as pending.
        """

        # ------------------------------------------------------
        # Prevent self-referral
        # ------------------------------------------------------

        if referrer.id == referred.id:
            raise ValueError(
                "A guest cannot refer themselves."
            )

        # ------------------------------------------------------
        # Prevent referred guest from having another referrer
        # ------------------------------------------------------

        existing_referral = (
            self.repository.get_by_referred_guest(
                referred_guest_id=referred.id,
            )
        )

        if existing_referral is not None:
            raise ValueError(
                "This guest has already been referred."
            )

        # ------------------------------------------------------
        # Defensive duplicate check
        # ------------------------------------------------------

        existing_relationship = (
            self.repository.get_by_referrer_and_referred(
                referrer_guest_id=referrer.id,
                referred_guest_id=referred.id,
            )
        )

        if existing_relationship is not None:
            raise ValueError(
                "This referral already exists."
            )

        # ------------------------------------------------------
        # Create referral
        # ------------------------------------------------------

        referral = Referral(
            referrer_guest_id=referrer.id,
            referred_guest_id=referred.id,
            status=self.PENDING,
            reward_granted=False,
        )

        self.repository.create(referral)

        self.db.commit()
        self.db.refresh(referral)

        return referral

    # ==========================================================
    # Qualification
    # ==========================================================

    def complete_referral(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Mark a pending referral as completed.

        This method does NOT grant the reward.

        Qualification and reward remain separate operations.
        """

        if referral.status == self.COMPLETED:
            return referral

        if referral.reward_granted:
            raise ValueError(
                "A rewarded referral cannot be completed again."
            )

        referral.status = self.COMPLETED

        self.repository.update(referral)

        self.db.commit()
        self.db.refresh(referral)

        return referral

    # ==========================================================
    # Reward
    # ==========================================================

    def grant_reward(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Mark a completed referral as rewarded.

        This method records referral reward state.

        The actual guest usage/credit event should be handled
        by GuestUsageService so referral logic does not create
        a second credit system.
        """

        # ------------------------------------------------------
        # Referral must be completed first
        # ------------------------------------------------------

        if referral.status != self.COMPLETED:
            raise ValueError(
                "Referral is not eligible for reward."
            )

        # ------------------------------------------------------
        # Prevent duplicate reward
        # ------------------------------------------------------

        if referral.reward_granted:
            raise ValueError(
                "Referral reward has already been granted."
            )

        # ------------------------------------------------------
        # Grant referral reward
        # ------------------------------------------------------

        referral.reward_granted = True
        referral.rewarded_at = datetime.now(timezone.utc)

        self.repository.update(referral)

        self.db.commit()
        self.db.refresh(referral)

        return referral

    # ==========================================================
    # Convenience
    # ==========================================================

    def get_referral(
        self,
        referral_id: str,
    ) -> Referral | None:
        """
        Return a referral by ID.
        """

        return self.repository.get_by_id(
            referral_id
        )

    def get_referrer_referrals(
        self,
        guest: Guest,
    ) -> list[Referral]:
        """
        Return all referrals created by a guest.
        """

        return self.repository.get_by_referrer(
            referrer_guest_id=guest.id
        )