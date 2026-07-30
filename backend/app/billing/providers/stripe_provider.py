from __future__ import annotations

import logging
from typing import Any

import stripe

from app.core.config import settings

from .base_provider import BasePaymentProvider


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

        stripe.api_key = settings.STRIPE_SECRET_KEY

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

            customer = stripe.Customer.create(
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
    ) -> dict[str, Any]:

        try:

            session = stripe.checkout.Session.create(
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
                billing_address_collection="auto",
                allow_promotion_codes=True,
                automatic_tax={
                    "enabled": True,
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

            session = (
                stripe.billing_portal.Session.create(
                    customer=customer_id,
                    return_url=return_url,
                )
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

            stripe.Subscription.delete(
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

            subscription = (
                stripe.Subscription.retrieve(
                    subscription_id
                )
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

            event = (
                stripe.Webhook.construct_event(
                    payload,
                    signature,
                    settings.STRIPE_WEBHOOK_SECRET,
                )
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

            refund = stripe.Refund.create(
                payment_intent=payment_id,
            )

            return dict(refund)

        except stripe.StripeError:

            logger.exception(
                "Stripe refund creation failed"
            )

            raise