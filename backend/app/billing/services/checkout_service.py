from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)
from app.billing.repository.database_pricing_repository import (
    DatabasePricingRepository,
)
from app.billing.services.billing_service import BillingService
from app.database.models.order import Order


class CheckoutService:
    """
    Application-level checkout orchestration.

    Responsibilities:

        1. Resolve pricing.
        2. Select the requested billing interval.
        3. Create the local pending order.
        4. Create/reuse the provider customer.
        5. Create the provider checkout session.
        6. Store the provider checkout/session ID.
        7. Return checkout information.

    This service does not communicate with Stripe directly.

    Provider-specific operations are delegated to BillingService.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

        self.pricing = DatabasePricingRepository(
            db,
        )

        self.orders = DatabaseOrderRepository(
            db,
        )

        self.billing = BillingService()

    # ==========================================================
    # Checkout
    # ==========================================================

    async def create_checkout(
        self,
        *,
        user_id: str,
        email: str,
        name: str,
        plan_code: str,
        country: str,
        interval: str,
        success_url: str,
        cancel_url: str,
        provider: str = "stripe",
    ) -> dict:
        """
        Create a local order and provider checkout session.

        The local order remains pending until the payment provider
        confirms successful payment through a webhook.

        Returns:

            {
                "order_id": "...",
                "customer_id": "...",
                "checkout_session_id": "...",
                "checkout_url": "...",
                "provider": "...",
                "country": "...",
                "plan": "...",
                "interval": "...",
                "price": 0.0,
                "currency": "INR",
            }
        """

        # ------------------------------------------------------
        # Normalize input
        # ------------------------------------------------------

        country = country.strip().upper()
        plan_code = plan_code.strip()
        interval = interval.strip().lower()
        provider = provider.strip().lower()

        # ------------------------------------------------------
        # Validate interval
        # ------------------------------------------------------

        if interval not in {"monthly", "yearly"}:
            raise ValueError(
                "Invalid billing interval. "
                "Expected 'monthly' or 'yearly'."
            )

        # ------------------------------------------------------
        # Pricing
        # ------------------------------------------------------

        pricing = self.pricing.get(
            plan_code=plan_code,
            country=country,
        )

        if pricing is None:
            raise ValueError(
                "Pricing not found for the selected plan and country."
            )

        # ------------------------------------------------------
        # Provider validation
        # ------------------------------------------------------

        if pricing.payment_provider.strip().lower() != provider:
            raise ValueError(
                "The selected payment provider is not configured "
                "for this pricing."
            )

        # ------------------------------------------------------
        # Select billing price
        # ------------------------------------------------------

        if interval == "yearly":

            if pricing.yearly_price is None:
                raise ValueError(
                    "Yearly pricing is not available for this plan."
                )

            price: Decimal = pricing.yearly_price
            price_id = pricing.stripe_yearly_price_id

        else:

            price = pricing.monthly_price
            price_id = pricing.stripe_monthly_price_id

        # ------------------------------------------------------
        # Validate provider price
        # ------------------------------------------------------

        if not price_id:
            raise ValueError(
                f"No {interval} Stripe price is configured "
                f"for plan '{plan_code}' in country '{country}'."
            )

        # ------------------------------------------------------
        # Create local pending order
        # ------------------------------------------------------

        order = Order(
            user_id=user_id,
            pricing_id=pricing.id,
            provider=provider,
            amount=price,
            currency=pricing.currency_code,
            status="pending",
        )

        order = self.orders.create(
            order,
        )

        # ------------------------------------------------------
        # Create provider customer
        # ------------------------------------------------------

        customer_id = await self.billing.create_customer(
            email=email,
            name=name,
            provider=provider,
        )

        # ------------------------------------------------------
        # Create provider checkout session
        # ------------------------------------------------------

        try:

           session = await self.billing.create_checkout_session(
    customer_id=customer_id,
    price_id=price_id,
    success_url=success_url,
    cancel_url=cancel_url,
    client_reference_id=order.id,
    metadata={
        "order_id": order.id,
        "user_id": user_id,
        "pricing_id": pricing.id,
        "plan_code": plan_code,
        "country": country,
        "interval": interval,
    },
    provider=provider,
)
        except Exception:
            # The order was created locally but checkout creation
            # failed. Roll back the local transaction so we do not
            # leave an unusable pending order behind.
            self.db.rollback()
            raise

        # ------------------------------------------------------
        # Validate provider response
        # ------------------------------------------------------

        checkout_session_id = session.get("id")
        checkout_url = session.get("url")

        if not checkout_session_id:
            self.db.rollback()

            raise ValueError(
                "Payment provider did not return a checkout session ID."
            )

        if not checkout_url:
            self.db.rollback()

            raise ValueError(
                "Payment provider did not return a checkout URL."
            )

        # ------------------------------------------------------
        # Save provider checkout/session ID
        # ------------------------------------------------------

        order.provider_order_id = checkout_session_id

        self.orders.update(
            order,
        )

        # ------------------------------------------------------
        # Commit local checkout state
        # ------------------------------------------------------

        self.db.commit()

        # ------------------------------------------------------
        # Return checkout information
        # ------------------------------------------------------

        return {
            "order_id": order.id,
            "customer_id": customer_id,
            "checkout_session_id": checkout_session_id,
            "checkout_url": checkout_url,
            "provider": provider,
            "country": country,
            "plan": plan_code,
            "interval": interval,
            "price": float(price),
            "currency": pricing.currency_code,
        }