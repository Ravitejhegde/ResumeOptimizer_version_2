from app.billing.services.billing_service import (
    BillingService,
)


class SubscriptionService:
    """
    Handles subscription operations.

    Business logic should use this service
    instead of talking directly to Stripe.
    """

    def __init__(self):

        self.billing = BillingService()

    async def get(
        self,
        subscription_id: str,
    ) -> dict:

        return await self.billing.get_subscription(

            subscription_id=subscription_id,

        )

    async def cancel(
        self,
        subscription_id: str,
    ) -> dict:

        await self.billing.cancel_subscription(

            subscription_id=subscription_id,

        )

        return {

            "success": True,

            "subscription_id": subscription_id,

            "message": "Subscription cancelled.",

        }

    async def status(
        self,
        subscription_id: str,
    ) -> str:

        subscription = await self.get(

            subscription_id,

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

            subscription_id,

        )

        return status in {

            "active",

            "trialing",

        }

    async def period(
        self,
        subscription_id: str,
    ) -> dict:

        subscription = await self.get(

            subscription_id,

        )

        return {

            "start": subscription.get(

                "current_period_start",

            ),

            "end": subscription.get(

                "current_period_end",

            ),

        }




