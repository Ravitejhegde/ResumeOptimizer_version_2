from __future__ import annotations

import logging
from typing import Any

from app.billing.providers.base_provider import (
    BasePaymentProvider,
)

from app.billing.providers.stripe_provider import (
    StripeProvider,
)


logger = logging.getLogger(__name__)


class BillingService:
    """
    Central billing service.

    All application billing operations
    must go through this class.

    Responsibilities:
    - Provider selection
    - Customer creation
    - Checkout creation
    - Subscription management
    - Refund handling
    - Webhook verification

    Routes and other services should never
    call payment providers directly.
    """

    def __init__(self) -> None:

        self._providers: dict[
            str,
            BasePaymentProvider,
        ] = {
            "stripe": StripeProvider(),
        }

    # ==========================================================
    # Provider Management
    # ==========================================================

    def provider(
        self,
        provider: str = "stripe",
    ) -> BasePaymentProvider:
        """
        Returns payment provider instance.
        """

        payment_provider = (
            self._providers.get(provider)
        )

        if payment_provider is None:
            raise ValueError(
                f"Unsupported payment provider: {provider}"
            )

        return payment_provider

    # ==========================================================
    # Customer
    # ==========================================================

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

    # ==========================================================
    # Checkout
    # ==========================================================

    async def create_checkout_session(
        self,
        *,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        provider: str = "stripe",
    ) -> Any:

        return await self.provider(
            provider
        ).create_checkout_session(
            customer_id=customer_id,
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

    # ==========================================================
    # Billing Portal
    # ==========================================================

    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
        provider: str = "stripe",
    ) -> Any:

        return await self.provider(
            provider
        ).create_billing_portal(
            customer_id=customer_id,
            return_url=return_url,
        )

    # ==========================================================
    # Subscription
    # ==========================================================

    async def get_subscription(
        self,
        *,
        subscription_id: str,
        provider: str = "stripe",
    ) -> Any:

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
    ) -> Any:

        return await self.provider(
            provider
        ).cancel_subscription(
            subscription_id=subscription_id,
        )

    # ==========================================================
    # Webhooks
    # ==========================================================

    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
        provider: str = "stripe",
    ) -> Any:

        return await self.provider(
            provider
        ).verify_webhook(
            payload=payload,
            signature=signature,
        )

    # ==========================================================
    # Refunds
    # ==========================================================

    async def create_refund(
        self,
        *,
        payment_id: str,
        provider: str = "stripe",
    ) -> Any:

        return await self.provider(
            provider
        ).create_refund(
            payment_id=payment_id,
        )