from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.database.models.usage_event import UsageEvent
from app.database.repositories.usage_repository import UsageRepository


# ============================================================
# Guest Usage Configuration
# ============================================================

GUEST_INITIAL_FREE_SAMPLES = 3

GUEST_SHARE_REWARD_SAMPLES = 2

GUEST_MAX_SHARE_REWARDS = 5


class GuestUsageService:
    """
    Business logic for anonymous guest optimization usage.

    Guests are completely separate from registered users,
    subscriptions, plans, billing, and paid credits.

    Guest usage is calculated as:

        Initial free samples
        + share rewards
        - completed optimizations

    Example:

        Initial samples = 3

        Guest shares 1 time:
            +2 samples
            = 5 total samples

        Guest shares 5 times:
            +10 samples
            = 13 total samples maximum

    Share rewards are limited to one successful claim
    per guest session and five successful claims per guest.
    """

    OPTIMIZATION_EVENT = "optimization_completed"
    SHARE_REWARD_EVENT = "share_reward_earned"

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db
        self.usage_repository = UsageRepository(db)

    # ========================================================
    # Usage
    # ========================================================

    def get_usage(
        self,
        guest: Guest,
    ) -> dict:
        """
        Return the current guest usage state.

        This method does not modify database state.
        """

        # ----------------------------------------------------
        # Count completed optimizations
        # ----------------------------------------------------

        optimization_count = (
            self.usage_repository.count_guest_events(
                guest_id=guest.id,
                event_type=self.OPTIMIZATION_EVENT,
            )
        )

        # ----------------------------------------------------
        # Count successful share rewards
        # ----------------------------------------------------

        share_reward_count = (
            self.usage_repository.count_guest_events(
                guest_id=guest.id,
                event_type=self.SHARE_REWARD_EVENT,
            )
        )

        # ----------------------------------------------------
        # Apply maximum reward limit
        # ----------------------------------------------------

        applied_share_rewards = min(
            share_reward_count,
            GUEST_MAX_SHARE_REWARDS,
        )

        # ----------------------------------------------------
        # Calculate earned samples
        # ----------------------------------------------------

        earned_samples = (
            applied_share_rewards
            * GUEST_SHARE_REWARD_SAMPLES
        )

        # ----------------------------------------------------
        # Calculate total available samples
        # ----------------------------------------------------

        total_samples = (
            GUEST_INITIAL_FREE_SAMPLES
            + earned_samples
        )

        # ----------------------------------------------------
        # Calculate remaining samples
        # ----------------------------------------------------

        remaining_samples = max(
            total_samples - optimization_count,
            0,
        )

        return {
            "is_guest": True,
            "free_samples": GUEST_INITIAL_FREE_SAMPLES,
            "used_samples": optimization_count,
            "earned_samples": earned_samples,
            "remaining_samples": remaining_samples,
            "can_optimize": remaining_samples > 0,
            "share_rewards": applied_share_rewards,
            "max_share_rewards": GUEST_MAX_SHARE_REWARDS,
        }

    # ========================================================
    # Permission
    # ========================================================

    def can_optimize(
        self,
        guest: Guest,
    ) -> bool:
        """
        Return True when the guest has at least one
        optimization sample remaining.
        """

        return self.get_usage(guest)["can_optimize"]

    # ========================================================
    # Session Validation
    # ========================================================

    def _get_valid_session(
        self,
        guest: Guest,
        guest_session_id: str,
    ) -> GuestSession:
        """
        Validate that the supplied guest session:

        1. Exists.
        2. Belongs to the supplied guest.
        3. Is currently active.

        Raises:
            ValueError: If the session is invalid.
        """

        session = (
            self.db.query(GuestSession)
            .filter(
                GuestSession.id == guest_session_id,
                GuestSession.guest_id == guest.id,
                GuestSession.active.is_(True),
            )
            .first()
        )

        if session is None:
            raise ValueError(
                "Invalid guest session."
            )

        return session

    # ========================================================
    # Consume Optimization
    # ========================================================

    def consume_optimization(
        self,
        guest: Guest,
        guest_session_id: str,
    ) -> UsageEvent:
        """
        Record one successfully completed guest optimization.

        The supplied session must belong to the guest.

        Usage is consumed only after the caller has determined
        that the optimization itself completed successfully.
        """

        # ----------------------------------------------------
        # Validate session ownership
        # ----------------------------------------------------

        self._get_valid_session(
            guest=guest,
            guest_session_id=guest_session_id,
        )

        # ----------------------------------------------------
        # Check available usage
        # ----------------------------------------------------

        if not self.can_optimize(guest):
            raise ValueError(
                "Guest optimization limit reached."
            )

        # ----------------------------------------------------
        # Record optimization usage
        # ----------------------------------------------------

        event = UsageEvent(
            guest_session_id=guest_session_id,
            event_type=self.OPTIMIZATION_EVENT,
            resource_type="resume",
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    # ========================================================
    # Share Reward
    # ========================================================

    def record_share_reward(
        self,
        guest: Guest,
        guest_session_id: str,
    ) -> UsageEvent:
        """
        Record one successful guest share reward.

        Reward rules:

        1. Session must exist.
        2. Session must belong to the guest.
        3. Session must be active.
        4. The same session can claim only once.
        5. Guest-wide reward limit is five claims.
        6. One successful claim awards two samples.

        The reward is represented as a UsageEvent.
        """

        # ----------------------------------------------------
        # Validate session
        # ----------------------------------------------------

        self._get_valid_session(
            guest=guest,
            guest_session_id=guest_session_id,
        )

        # ----------------------------------------------------
        # Prevent duplicate claim from the same session
        # ----------------------------------------------------

        already_claimed = (
            self.usage_repository.guest_session_has_event(
                guest_session_id=guest_session_id,
                event_type=self.SHARE_REWARD_EVENT,
            )
        )

        if already_claimed:
            raise ValueError(
                "Share reward already claimed for this session."
            )

        # ----------------------------------------------------
        # Enforce guest-wide reward limit
        # ----------------------------------------------------

        current_rewards = (
            self.usage_repository.count_guest_events(
                guest_id=guest.id,
                event_type=self.SHARE_REWARD_EVENT,
            )
        )

        if current_rewards >= GUEST_MAX_SHARE_REWARDS:
            raise ValueError(
                "Maximum guest sharing rewards reached."
            )

        # ----------------------------------------------------
        # Create reward event
        # ----------------------------------------------------

        event = UsageEvent(
            guest_session_id=guest_session_id,
            event_type=self.SHARE_REWARD_EVENT,
            resource_type="guest_share",
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event