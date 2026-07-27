from typing import Any

import stripe

from app.core.config import settings

from .base_provider import BasePaymentProvider


class StripeProvider(BasePaymentProvider):
    """
    Stripe payment provider.
    """

    def __init__(self):

        stripe.api_key = settings.STRIPE_SECRET_KEY

    async def create_customer(
        self,
        *,
        email: str,
        name: str,
    ) -> str:

        customer = stripe.Customer.create(

            email=email,

            name=name,

        )

        return customer.id

    async def create_checkout_session(
        self,
        *,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
    ) -> dict[str, Any]:

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

    async def create_billing_portal(
        self,
        *,
        customer_id: str,
        return_url: str,
    ) -> str:

        session = stripe.billing_portal.Session.create(

            customer=customer_id,

            return_url=return_url,

        )

        return session.url

    async def cancel_subscription(
        self,
        *,
        subscription_id: str,
    ) -> None:

        stripe.Subscription.delete(

            subscription_id,

        )

    async def get_subscription(
        self,
        *,
        subscription_id: str,
    ) -> dict[str, Any]:

        subscription = stripe.Subscription.retrieve(

            subscription_id,

        )

        return subscription

    async def verify_webhook(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> dict[str, Any]:

        event = stripe.Webhook.construct_event(

            payload=payload,

            sig_header=signature,

            secret=settings.STRIPE_WEBHOOK_SECRET,

        )

        return event

    async def create_refund(
        self,
        *,
        payment_id: str,
    ) -> dict[str, Any]:

        refund = stripe.Refund.create(

            payment_intent=payment_id,

        )

        return refund




