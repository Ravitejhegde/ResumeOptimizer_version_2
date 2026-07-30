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

    The application should never depend
    directly on a payment provider.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns provider name.
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
        Creates a customer.

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
    ) -> dict[str, Any]:
        """
        Creates a checkout session.

        Returns:
            Provider checkout information.
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
        Creates customer billing portal.

        Returns:
            Portal URL.
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
        Retrieves subscription information.
        """
        raise NotImplementedError

    @abstractmethod
    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
    ) -> None:
        """
        Cancels subscription.
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
        Verifies webhook signature.

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
        Creates payment refund.

        Returns:
            Refund information.
        """
        raise NotImplementedError