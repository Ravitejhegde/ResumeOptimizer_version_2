from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.usage_event import UsageEvent


# ============================================================
# Guest Usage Configuration
# ============================================================

GUEST_INITIAL_FREE_SAMPLES = 3
GUEST_SHARE_REWARD_SAMPLES = 2
GUEST_MAX_SHARE_REWARDS = 5


class GuestUsageService:
    """
    Handles anonymous guest optimization usage.

    Guests do not have subscriptions.

    Their available usage is calculated from:
        initial free samples
        + sharing rewards
        - completed optimizations
    """

    OPTIMIZATION_EVENT = "optimization_completed"
    SHARE_REWARD_EVENT = "share_reward_earned"

    def __init__(self, db: Session) -> None:
        self.db = db

    # ========================================================
    # Usage
    # ========================================================

    def get_usage(
        self,
        guest: Guest,
    ) -> dict:
        """
        Return the current usage state for a guest.
        """

        optimization_count = (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.event_type == self.OPTIMIZATION_EVENT,
                UsageEvent.guest_session_id.isnot(None),
            )
            .join(
                UsageEvent.guest_session,
            )
            .filter(
                UsageEvent.guest_session.has(
                    guest_id=guest.id,
                )
            )
            .count()
        )

        share_reward_count = (
            self.db.query(UsageEvent)
            .filter(
                UsageEvent.event_type == self.SHARE_REWARD_EVENT,
            )
            .join(
                UsageEvent.guest_session,
            )
            .filter(
                UsageEvent.guest_session.has(
                    guest_id=guest.id,
                )
            )
            .count()
        )

        # Never allow more sharing rewards than configured.
        applied_share_rewards = min(
            share_reward_count,
            GUEST_MAX_SHARE_REWARDS,
        )

        earned_samples = (
            applied_share_rewards
            * GUEST_SHARE_REWARD_SAMPLES
        )

        total_samples = (
            GUEST_INITIAL_FREE_SAMPLES
            + earned_samples
        )

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
        Return whether the guest can perform another optimization.
        """

        usage = self.get_usage(guest)

        return usage["can_optimize"]

    # ========================================================
    # Consume optimization
    # ========================================================

    def consume_optimization(
        self,
        guest_session_id: str,
    ) -> UsageEvent:
        """
        Record a successfully completed optimization.

        Important:
        This method records usage only after the optimization
        actually succeeds.
        """

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
    # Share reward
    # ========================================================

    def record_share_reward(
        self,
        guest: Guest,
        guest_session_id: str,
    ) -> UsageEvent:
        """
        Record a successful sharing reward.

        The maximum number of rewards is enforced per guest.
        """

        current_rewards = (
            self.db.query(UsageEvent)
            .join(
                UsageEvent.guest_session,
            )
            .filter(
                UsageEvent.event_type
                == self.SHARE_REWARD_EVENT,
                UsageEvent.guest_session.has(
                    guest_id=guest.id,
                ),
            )
            .count()
        )

        if current_rewards >= GUEST_MAX_SHARE_REWARDS:
            raise ValueError(
                "Maximum guest sharing rewards reached."
            )

        event = UsageEvent(
            guest_session_id=guest_session_id,
            event_type=self.SHARE_REWARD_EVENT,
            resource_type="guest_share",
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event