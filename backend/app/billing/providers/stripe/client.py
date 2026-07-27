import stripe

from app.core.config import settings


class StripeClient:
    """
    Shared Stripe client.
    """

    def __init__(self):

        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.api_version = settings.STRIPE_API_VERSION

        self.client = stripe




