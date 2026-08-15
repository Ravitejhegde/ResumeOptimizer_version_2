from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.referral import Referral
from app.database.models.guest_session import GuestSession
from app.database.models.usage_event import UsageEvent
from app.database.repositories.referral_repository import (
    ReferralRepository,
)


REFERRAL_REWARD_SAMPLES = 2
REFERRAL_REWARD_EVENT = "share_reward_earned"


class ReferralService:
    """
    Business logic for guest referrals.

    Referral lifecycle:

        pending
            ↓
        completed
            ↓
        reward granted

    A completed referral grants exactly two samples
    to the referrer guest.
    """

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
        Create a pending referral relationship.
        """

        if referrer.id == referred.id:
            raise ValueError(
                "A guest cannot refer themselves."
            )

        existing = self.repository.get_by_referred(
            referred.id,
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

        Completion alone does not grant the reward.
        Call grant_reward() after completion.
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
        Grant two samples to the referrer.

        The reward is represented by a UsageEvent belonging
        to the referrer's guest session.

        Reward is granted exactly once.
        """

        # ------------------------------------------------------
        # Referral must be completed
        # ------------------------------------------------------

        if referral.status != "completed":
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
        # Find referrer session
        #
        # We intentionally do NOT require active=True.
        #
        # A referral reward belongs to the referrer guest,
        # not necessarily the referrer's current browser session.
        # ------------------------------------------------------

        referrer_session = (
            self.db.query(
                GuestSession
            )
            .filter(
                GuestSession.guest_id
                == referral.referrer_guest_id,
            )
            .order_by(
                GuestSession.created_at.desc(),
            )
            .first()
        )

        if referrer_session is None:
            raise ValueError(
                "Referrer has no guest session."
            )

        # ------------------------------------------------------
        # Create reward event
        # ------------------------------------------------------

        reward_event = UsageEvent(
            guest_session_id=referrer_session.id,
            event_type=REFERRAL_REWARD_EVENT,
            resource_type="referral",
            resource_id=referral.id,
            event_metadata=json.dumps(
                {
                    "samples": REFERRAL_REWARD_SAMPLES,
                    "referral_id": referral.id,
                    "referred_guest_id": (
                        referral.referred_guest_id
                    ),
                }
            ),
        )

        self.db.add(reward_event)

        # ------------------------------------------------------
        # Mark referral rewarded
        # ------------------------------------------------------

        referral.reward_granted = True
        referral.rewarded_at = datetime.now(
            timezone.utc,
        )

        updated = self.repository.update(
            referral,
        )

        self.db.commit()
        self.db.refresh(updated)

        return updated