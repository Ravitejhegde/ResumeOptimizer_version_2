from abc import ABC, abstractmethod
from typing import Any


class BasePaymentProvider(ABC):
    """
    Base interface for all payment providers.

    StripeProvider
    RazorpayProvider
    PayPalProvider

    must implement this interface.
    """

    @abstractmethod
    async def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:
        """
        Create a customer.

        Returns provider customer id.
        """
        raise NotImplementedError

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
        Returns checkout session.
        """
        raise NotImplementedError

    @abstractmethod
    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
    ) -> str:
        """
        Returns billing portal URL.
        """
        raise NotImplementedError

    @abstractmethod
    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
    ) -> None:
        """
        Cancel subscription.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_subscription(
        self,
        *,
        subscription_id: str,
    ) -> dict[str, Any]:
        """
        Returns subscription details.
        """
        raise NotImplementedError

    @abstractmethod
    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict[str, Any]:
        """
        Verify webhook signature.

        Returns webhook event.
        """
        raise NotImplementedError

    @abstractmethod
    async def create_refund(
        self,
        *,
        payment_id: str,
    ) -> dict[str, Any]:
        """
        Refund payment.
        """
        raise NotImplementedError




