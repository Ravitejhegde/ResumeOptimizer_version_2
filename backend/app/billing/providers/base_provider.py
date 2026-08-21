from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePaymentProvider(ABC):
    """
    Abstract interface for payment providers.

    Implementations:
        - StripeProvider
        - RazorpayProvider
        - PayPalProvider

    Application/business logic must not depend directly
    on a specific payment provider.
    """

    # ==========================================================
    # Provider Information
    # ==========================================================

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the provider name.
        """
        raise NotImplementedError

    # ==========================================================
    # Customer
    # ==========================================================

    @abstractmethod
    async def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:
        """
        Create a customer with the payment provider.

        Returns:
            Provider customer ID.
        """
        raise NotImplementedError

    # ==========================================================
    # Checkout
    # ==========================================================

    @abstractmethod
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
    ) -> dict[str, Any]:
        """
        Create a subscription checkout session.

        Args:
            customer_id:
                Provider customer ID.

            price_id:
                Provider price ID.

            success_url:
                URL to redirect to after successful checkout.

            cancel_url:
                URL to redirect to if checkout is cancelled.

            client_reference_id:
                Application-side reference, normally the local
                order ID.

            metadata:
                Metadata to attach to the checkout session.

            allow_promotion_codes:
                Whether customers can enter promotion codes.

            automatic_tax:
                Whether automatic tax calculation is enabled.

        Returns:
            Dictionary containing provider checkout information.

            Expected structure:

                {
                    "id": "...",
                    "url": "..."
                }
        """
        raise NotImplementedError

    # ==========================================================
    # Billing Portal
    # ==========================================================

    @abstractmethod
    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
    ) -> str:
        """
        Create a customer billing portal session.

        Returns:
            Billing portal URL.
        """
        raise NotImplementedError

    # ==========================================================
    # Subscription
    # ==========================================================

    @abstractmethod
    async def get_subscription(
        self,
        *,
        subscription_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve subscription information.

        Returns:
            Provider subscription information.
        """
        raise NotImplementedError

    @abstractmethod
    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
    ) -> None:
        """
        Cancel a subscription.
        """
        raise NotImplementedError

    # ==========================================================
    # Webhooks
    # ==========================================================

    @abstractmethod
    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict[str, Any]:
        """
        Verify a provider webhook signature.

        Returns:
            Parsed webhook event.
        """
        raise NotImplementedError

    # ==========================================================
    # Refunds
    # ==========================================================

    @abstractmethod
    async def create_refund(
        self,
        *,
        payment_id: str,
    ) -> dict[str, Any]:
        """
        Create a refund.

        Args:
            payment_id:
                Provider payment/payment-intent identifier.

        Returns:
            Provider refund information.
        """
        raise NotImplementedError