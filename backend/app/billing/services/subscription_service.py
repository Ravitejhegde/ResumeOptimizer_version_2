from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.billing.services.billing_service import (
    BillingService,
)

from app.database.models.subscription import (
    Subscription,
)

from app.database.repositories.subscription_repository import (
    SubscriptionRepository,
)


logger = logging.getLogger(__name__)


class SubscriptionService:
    """
    Handles subscription business logic.

    Responsibilities:

    - Communicate with billing provider
    - Manage application subscriptions
    - Check subscription status
    - Cancel subscriptions
    - Sync subscription state
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.subscriptions = (
            SubscriptionRepository(db)
        )

        self.billing = BillingService()

    # ==========================================================
    # Provider Operations
    # ==========================================================

    async def get_remote_subscription(
        self,
        subscription_id: str,
    ) -> dict:

        return await self.billing.get_subscription(
            subscription_id=subscription_id,
        )

    async def cancel_remote_subscription(
        self,
        subscription_id: str,
    ) -> None:

        await self.billing.cancel_subscription(
            subscription_id=subscription_id,
        )

    # ==========================================================
    # Local Subscription
    # ==========================================================

    def get_user_subscription(
        self,
        user_id: str,
    ) -> Subscription | None:

        return self.subscriptions.get_active(
            user_id
        )

    def cancel_local_subscription(
        self,
        subscription: Subscription,
    ) -> Subscription:

        subscription.status = "cancelled"

        subscription.cancelled_at = (
            datetime.now(timezone.utc)
        )

        return self.subscriptions.update(
            subscription
        )

    # ==========================================================
    # Status
    # ==========================================================

    async def status(
        self,
        subscription_id: str,
    ) -> str:

        subscription = (
            await self.get_remote_subscription(
                subscription_id
            )
        )

        return subscription.get(
            "status",
            "unknown",
        )

    async def is_active(
        self,
        subscription_id: str,
    ) -> bool:

        status = await self.status(
            subscription_id
        )

        return status in {
            "active",
            "trialing",
        }

    # ==========================================================
    # Period
    # ==========================================================

    async def period(
        self,
        subscription_id: str,
    ) -> dict:

        subscription = (
            await self.get_remote_subscription(
                subscription_id
            )
        )

        return {
            "start": subscription.get(
                "current_period_start"
            ),
            "end": subscription.get(
                "current_period_end"
            ),
        }

    # ==========================================================
    # Sync
    # ==========================================================

    async def sync_status(
        self,
        subscription_id: str,
        local_subscription: Subscription,
    ) -> Subscription:

        status = await self.status(
            subscription_id
        )

        local_subscription.status = status

        period = await self.period(
            subscription_id
        )

        if period["end"]:
            local_subscription.expires_at = (
                datetime.fromtimestamp(
                    period["end"],
                    tz=timezone.utc,
                )
            )

        return self.subscriptions.update(
            local_subscription
        )