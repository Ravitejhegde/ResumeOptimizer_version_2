from sqlalchemy.orm import Session

from app.billing.providers.stripe.customer import (
    StripeCustomer,
)

from app.billing.providers.stripe.checkout import (
    StripeCheckout,
)

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)

from app.billing.repository.database_pricing_repository import (
    DatabasePricingRepository,
)

from app.database.models.order import Order


class CheckoutService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.customers = StripeCustomer()

        self.checkout = StripeCheckout()

        self.orders = DatabaseOrderRepository(db)

        self.pricing = DatabasePricingRepository(db)

    def create_checkout(

        self,

        user_id: str,

        email: str,

        plan_code: str,

        country: str,

        interval: str,

        success_url: str,

        cancel_url: str,

    ):

        # -------------------------------------
        # Pricing
        # -------------------------------------

        pricing = self.pricing.get(

            plan_code,

            country,

        )

        if pricing is None:

            raise ValueError(

                "Pricing not found."

            )

        # -------------------------------------
        # Customer
        # -------------------------------------

        customer = self.customers.search(
            email
        )

        if customer is None:

            customer = self.customers.create(

                email=email,

                name=email,

            )

        # -------------------------------------
        # Price
        # -------------------------------------

        if interval == "yearly":

            price = float(
                pricing.yearly_price
            )

            price_id = (
                pricing.stripe_yearly_price_id
            )

        else:

            price = float(
                pricing.monthly_price
            )

            price_id = (
                pricing.stripe_monthly_price_id
            )

        # -------------------------------------
        # Order
        # -------------------------------------

        order = Order(

            user_id=user_id,

            pricing_id=pricing.id,

            provider="stripe",

            amount=price,

            currency=pricing.currency_code,

            status="pending",

        )

        order = self.orders.create(
            order
        )

        # -------------------------------------
        # Stripe Checkout
        # -------------------------------------

        session = self.checkout.create(

            customer=customer.id,

            price_id=price_id,

            success_url=success_url,

            cancel_url=cancel_url,

            client_reference_id=order.id,

            metadata={

                "order_id": order.id,

                "user_id": user_id,

            },

        )

        order.provider_order_id = (
            session.id
        )

        self.orders.update(order)

        return {

            "checkout_url": session.url,

            "order_id": order.id,

            "session_id": session.id,

        }