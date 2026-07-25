from app.billing.providers.base_provider import (
    BasePaymentProvider,
)

from app.billing.providers.stripe_provider import (
    StripeProvider,
)


class BillingService:
    """
    Central billing service.

    The rest of the application should ONLY use this class.

    Never call Stripe directly from routes,
    repositories or business logic.
    """

    def __init__(self):

        self._providers = {

            "stripe": StripeProvider(),

        }

    def provider(
        self,
        provider: str = "stripe",
    ) -> BasePaymentProvider:

        if provider not in self._providers:

            raise ValueError(

                f"Unsupported payment provider: {provider}"

            )

        return self._providers[provider]

    async def create_customer(
        self,
        *,
        email: str,
        name: str,
        provider: str = "stripe",
    ) -> str:

        return await self.provider(
            provider
        ).create_customer(

            email=email,

            name=name,

        )

    async def create_checkout_session(
        self,
        *,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).create_checkout_session(

            customer_id=customer_id,

            price_id=price_id,

            success_url=success_url,

            cancel_url=cancel_url,

        )

    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).create_billing_portal(

            customer_id=customer_id,

            return_url=return_url,

        )

    async def get_subscription(
        self,
        *,
        subscription_id: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).get_subscription(

            subscription_id=subscription_id,

        )

    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).cancel_subscription(

            subscription_id=subscription_id,

        )

    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).verify_webhook(

            payload=payload,

            signature=signature,

        )

    async def create_refund(
        self,
        *,
        payment_id: str,
        provider: str = "stripe",
    ):

        return await self.provider(
            provider
        ).create_refund(

            payment_id=payment_id,

        )