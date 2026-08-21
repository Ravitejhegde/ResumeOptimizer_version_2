import stripe

from app.core.config import settings

from .client import StripeClient


class StripeWebhook:

    def __init__(self):

        self.stripe = (
            StripeClient().client
        )

    def verify(

        self,

        payload: bytes,

        signature: str,

    ):

        return stripe.Webhook.construct_event(

            payload=payload,

            sig_header=signature,

            secret=settings.STRIPE_WEBHOOK_SECRET,

        )

    def event_type(

        self,

        event,

    ) -> str:

        return event["type"]

    def data(

        self,

        event,

    ):

        return event["data"]["object"]

    def is_checkout_completed(

        self,

        event,

    ) -> bool:

        return (

            self.event_type(event)

            == "checkout.session.completed"

        )

    def is_invoice_paid(

        self,

        event,

    ) -> bool:

        return (

            self.event_type(event)

            == "invoice.paid"

        )

    def is_invoice_failed(

        self,

        event,

    ) -> bool:

        return (

            self.event_type(event)

            == "invoice.payment_failed"

        )

    def is_subscription_updated(

        self,

        event,

    ) -> bool:

        return (

            self.event_type(event)

            == "customer.subscription.updated"

        )

    def is_subscription_deleted(

        self,

        event,

    ) -> bool:

        return (

            self.event_type(event)

            == "customer.subscription.deleted"

        )

    def subscription(
        self,
        subscription_id: str,
    ) -> dict:
        """
        Retrieve a Stripe subscription by ID.
        """

        subscription = self.stripe.Subscription.retrieve(
            subscription_id
        )

        return dict(subscription)


