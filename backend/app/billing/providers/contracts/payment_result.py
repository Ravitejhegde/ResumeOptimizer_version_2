from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentSession:
    """
    Provider-neutral checkout session.

    Billing services use this object instead of depending
    on Stripe/Razorpay/etc. response objects.
    """

    session_id: str
    checkout_url: str
    provider: str
    provider_payment_id: str | None = None