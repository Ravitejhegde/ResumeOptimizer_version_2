from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.referral import Referral
from app.database.repositories.referral_repository import (
    ReferralRepository,
)


class ReferralService:
    """
    Business logic for guest referrals.
    """

    def __init__(self, db: Session) -> None:
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
        Create a pending referral relationship.
        """

        if referrer.id == referred.id:
            raise ValueError(
                "A guest cannot refer themselves."
            )

        existing = self.repository.get_by_referred(
            referred.id
        )

        if existing is not None:
            raise ValueError(
                "This guest has already been referred."
            )

        referral = Referral(
            referrer_guest_id=referrer.id,
            referred_guest_id=referred.id,
            status="pending",
            reward_granted=False,
        )

        return self.repository.create(referral)

    # ==========================================================
    # Complete Referral
    # ==========================================================

    def complete_referral(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Mark a pending referral as completed.
        """

        if referral.status != "pending":
            raise ValueError(
                "Referral is not pending."
            )

        referral.status = "completed"

        return self.repository.update(referral)

    # ==========================================================
    # Grant Reward
    # ==========================================================

    def grant_reward(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Grant the reward for a completed referral.
        """

        if referral.status != "completed":
            raise ValueError(
                "Referral is not eligible for reward."
            )

        if referral.reward_granted:
            raise ValueError(
                "Referral reward has already been granted."
            )

        referral.reward_granted = True
        referral.rewarded_at = datetime.now(timezone.utc)

        return self.repository.update(referral)