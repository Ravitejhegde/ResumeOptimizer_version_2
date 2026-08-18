from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.database.models.referral import Referral
from app.database.models.usage_event import UsageEvent
from app.database.repositories.referral_repository import (
    ReferralRepository,
)


# ============================================================
# Referral Configuration
# ============================================================

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
        reward_granted = True

    A referral is completed only after the referred guest
    successfully performs the required optimization.

    The reward belongs to the referrer guest.

    One successful referral grants exactly two samples.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db
        self.repository = ReferralRepository(db)

    # ========================================================
    # Create Referral
    # ========================================================

    def create_referral(
        self,
        referrer: Guest,
        referred: Guest,
    ) -> Referral:
        """
        Create a pending referral relationship.

        Rules:

        1. A guest cannot refer themselves.
        2. A referred guest can have only one referrer.
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

        return self.repository.create(
            referral,
        )

    # ========================================================
    # Complete Referral
    # ========================================================

    def complete_referral(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Mark a pending referral as completed.

        Completion itself does not create the reward.
        Use grant_reward() after completion.
        """

        if referral.status != "pending":
            raise ValueError(
                "Referral is not pending."
            )

        referral.status = "completed"

        return self.repository.update(
            referral,
        )

    # ========================================================
    # Grant Reward
    # ========================================================

    def grant_reward(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Grant the referral reward to the referrer.

        The reward is represented by a UsageEvent attached
        to one of the referrer's guest sessions.

        Rules:

        1. Referral must be completed.
        2. Referral must not already be rewarded.
        3. Referrer must have at least one guest session.
        4. Exactly one reward event is created.
        5. Referral and reward event are committed together.
        """

        # ----------------------------------------------------
        # 1. Referral must be completed
        # ----------------------------------------------------

        if referral.status != "completed":
            raise ValueError(
                "Referral is not eligible for reward."
            )

        # ----------------------------------------------------
        # 2. Prevent duplicate reward
        # ----------------------------------------------------

        if referral.reward_granted:
            raise ValueError(
                "Referral reward has already been granted."
            )

        # ----------------------------------------------------
        # 3. Find referrer session
        #
        # We intentionally do not require active=True.
        #
        # The reward belongs to the referrer guest, not
        # necessarily their currently active browser session.
        # ----------------------------------------------------

        referrer_session = (
            self.db.query(GuestSession)
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

        # ----------------------------------------------------
        # 4. Create reward event
        # ----------------------------------------------------

        reward_event = UsageEvent(
            guest_session_id=referrer_session.id,
            event_type=REFERRAL_REWARD_EVENT,
            resource_type="referral",
            resource_id=referral.id,
            event_metadata=json.dumps(
                {
                    "samples": REFERRAL_REWARD_SAMPLES,
                    "referral_id": referral.id,
                    "referrer_guest_id": (
                        referral.referrer_guest_id
                    ),
                    "referred_guest_id": (
                        referral.referred_guest_id
                    ),
                }
            ),
        )

        self.db.add(reward_event)

        # ----------------------------------------------------
        # 5. Mark referral as rewarded
        # ----------------------------------------------------

        referral.reward_granted = True
        referral.rewarded_at = datetime.now(
            timezone.utc,
        )

        self.repository.update(
            referral,
        )

        # ----------------------------------------------------
        # 6. Commit reward + referral together
        # ----------------------------------------------------

        self.db.commit()

        self.db.refresh(
            referral,
        )

        return referral

    # ========================================================
    # Complete + Reward
    # ========================================================

    def complete_and_reward(
        self,
        referred_guest_id: str,
    ) -> Referral | None:
        """
        Complete and reward the referral belonging to a
        successfully optimized referred guest.

        Returns:

            Referral
                When a referral exists and is completed/rewarded.

            None
                When the guest was not referred.

        Intended to be called only after the referred guest
        successfully completes an optimization.

        Repeated calls after the reward has already been granted
        are harmless.
        """

        # ----------------------------------------------------
        # 1. Find referral
        # ----------------------------------------------------

        referral = self.repository.get_by_referred(
            referred_guest_id,
        )

        if referral is None:
            return None

        # ----------------------------------------------------
        # 2. Already rewarded
        # ----------------------------------------------------

        if referral.reward_granted:
            return referral

        # ----------------------------------------------------
        # 3. Complete referral
        # ----------------------------------------------------

        self.complete_referral(
            referral,
        )

        # ----------------------------------------------------
        # 4. Grant reward
        # ----------------------------------------------------

        self.grant_reward(
            referral,
        )

        # grant_reward() commits and refreshes.
        return referral