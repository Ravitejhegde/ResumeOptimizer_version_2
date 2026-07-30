from sqlalchemy.orm import Session

from app.billing.providers.stripe_provider import (
    StripeProvider,
)
from app.billing.services.checkout_orchestrator import (
    CheckoutOrchestrator,
)
from app.database.models.order import Order


class StripeCheckoutService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.provider = StripeProvider()

        self.checkout = CheckoutOrchestrator(
            db
        )

    async def create_checkout(

        self,

        user_id: str,

        email: str,

        pricing,

        success_url: str,

        cancel_url: str,

    ) -> dict:

        # ---------------------------------------
        # Create Local Order
        # ---------------------------------------

        order: Order = self.checkout.create_order(

            user_id=user_id,

            pricing_id=pricing.id,

            amount=float(
                pricing.monthly_price
            ),

            currency=pricing.currency_code,

        )

        # ---------------------------------------
        # Create Stripe Checkout
        # ---------------------------------------

        session = await self.provider.create_checkout_session(

            customer_email=email,

            order_id=order.id,

            price_id=pricing.stripe_monthly_price_id,

            success_url=success_url,

            cancel_url=cancel_url,

        )

        # ---------------------------------------
        # Save Stripe Checkout ID
        # ---------------------------------------

        order.provider = "stripe"

        order.provider_order_id = session["id"]

        self.db.commit()

        return {

            "order_id": order.id,

            "checkout_url": session["url"],

            "checkout_session": session["id"],

        }




