from __future__ import annotations

import logging
from typing import Any

from app.billing.providers.base_provider import (
    BasePaymentProvider,
)
from app.billing.providers.stripe_provider import (
    StripeProvider,
)
from app.core.config import settings


logger = logging.getLogger(__name__)


class BillingService:
    """
    Central billing service.

    All application billing operations must go through
    this service.

    Responsibilities:
        - Provider selection
        - Customer creation
        - Checkout creation
        - Billing portal creation
        - Subscription management
        - Webhook verification
        - Refund handling

    Routes and other application services must not call
    payment providers directly.
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
        provider: str | None = None,
    ) -> BasePaymentProvider:
        """
        Return the configured payment provider.

        If provider is omitted, BILLING_PROVIDER from settings
        is used.
        """

        provider_name = (
            provider
            or settings.BILLING_PROVIDER
        ).strip().lower()

        payment_provider = self._providers.get(
            provider_name,
        )

        if payment_provider is None:
            raise ValueError(
                f"Unsupported payment provider: "
                f"{provider_name}"
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
        provider: str | None = None,
    ) -> str:
        """
        Create a customer through the selected provider.
        """

        payment_provider = self.provider(
            provider,
        )

        return await payment_provider.create_customer(
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
    client_reference_id: str | None = None,
    metadata: dict[str, str] | None = None,
    allow_promotion_codes: bool = True,
    automatic_tax: bool = True,
    provider: str | None = None,
) -> dict[str, Any]:

        return await self.provider(
        provider
    ).create_checkout_session(
        customer_id=customer_id,
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=client_reference_id,
        metadata=metadata,
        allow_promotion_codes=allow_promotion_codes,
        automatic_tax=automatic_tax,
    )

    # ==========================================================
    # Billing Portal
    # ==========================================================

    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
        provider: str | None = None,
    ) -> str:
        """
        Create a billing portal session through the selected
        payment provider.
        """

        payment_provider = self.provider(
            provider,
        )

        return await payment_provider.create_billing_portal(
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
        provider: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve a subscription from the payment provider.
        """

        payment_provider = self.provider(
            provider,
        )

        return await payment_provider.get_subscription(
            subscription_id=subscription_id,
        )

    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
        provider: str | None = None,
    ) -> None:
        """
        Cancel a subscription through the payment provider.
        """

        payment_provider = self.provider(
            provider,
        )

        await payment_provider.cancel_subscription(
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
        provider: str | None = None,
    ) -> dict[str, Any]:
        """
        Verify and parse a payment-provider webhook.
        """

        payment_provider = self.provider(
            provider,
        )

        return await payment_provider.verify_webhook(
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
        provider: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a refund through the selected payment provider.
        """

        payment_provider = self.provider(
            provider,
        )

        return await payment_provider.create_refund(
            payment_id=payment_id,
        )