from __future__ import annotations

import logging
from typing import Any

import stripe

from app.billing.providers.base_provider import BasePaymentProvider
from app.billing.providers.stripe.client import StripeClient
from app.core.config import settings


logger = logging.getLogger(__name__)


class StripeProvider(BasePaymentProvider):
    """
    Stripe payment provider implementation.

    This class only communicates with Stripe.

    Business logic belongs to:
        - CheckoutService
        - SubscriptionService
        - WebhookService
    """

    def __init__(self) -> None:
        self.stripe = StripeClient().client

    # ==========================================================
    # Provider Information
    # ==========================================================

    @property
    def name(self) -> str:
        return "stripe"

    # ==========================================================
    # Customer
    # ==========================================================

    async def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:
        try:
            customer = self.stripe.Customer.create(
                email=email,
                name=name,
            )

            return customer.id

        except stripe.StripeError:
            logger.exception(
                "Stripe customer creation failed"
            )
            raise

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
    ) -> dict[str, Any]:
        try:
            session = self.stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=client_reference_id,
                metadata=metadata or {},
                billing_address_collection="auto",
                allow_promotion_codes=allow_promotion_codes,
                automatic_tax={
                    "enabled": automatic_tax,
                },
            )

            return {
                "id": session.id,
                "url": session.url,
            }

        except stripe.StripeError:
            logger.exception(
                "Stripe checkout creation failed"
            )
            raise

    # ==========================================================
    # Billing Portal
    # ==========================================================

    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
    ) -> str:
        try:
            session = self.stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )

            return session.url

        except stripe.StripeError:
            logger.exception(
                "Stripe billing portal creation failed"
            )
            raise

    # ==========================================================
    # Subscription
    # ==========================================================

    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
    ) -> None:
        try:
            self.stripe.Subscription.delete(
                subscription_id
            )

        except stripe.StripeError:
            logger.exception(
                "Stripe subscription cancellation failed"
            )
            raise

    async def get_subscription(
        self,
        *,
        subscription_id: str,
    ) -> dict[str, Any]:
        try:
            subscription = self.stripe.Subscription.retrieve(
                subscription_id
            )

            return dict(subscription)

        except stripe.StripeError:
            logger.exception(
                "Stripe subscription retrieval failed"
            )
            raise

    # ==========================================================
    # Webhook
    # ==========================================================

    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict[str, Any]:
        try:
            event = self.stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
            )

            return dict(event)

        except stripe.StripeError:
            logger.exception(
                "Stripe webhook verification failed"
            )
            raise

    # ==========================================================
    # Refund
    # ==========================================================

    async def create_refund(
        self,
        *,
        payment_id: str,
    ) -> dict[str, Any]:
        try:
            refund = self.stripe.Refund.create(
                payment_intent=payment_id,
            )

            return dict(refund)

        except stripe.StripeError:
            logger.exception(
                "Stripe refund creation failed"
            )
            raise