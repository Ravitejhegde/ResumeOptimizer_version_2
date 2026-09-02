from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)
from typing import Literal


# ==========================================================
# Billing Interval
# ==========================================================

BillingInterval = Literal[
    "monthly",
    "yearly",
]


# ==========================================================
# Checkout Request
# ==========================================================

class CheckoutRequest(BaseModel):
    """
    Checkout request.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    country: str = Field(
        default="IN",
        min_length=2,
        max_length=2,
    )

    plan: str = Field(
        min_length=1,
        max_length=50,
    )

    interval: BillingInterval = Field(
        default="monthly",
    )

    provider: str = Field(
        default="stripe",
    )

    success_url: str

    cancel_url: str


# ==========================================================
# Checkout Response
# ==========================================================

class CheckoutResponse(BaseModel):
    """
    Checkout response.
    """

    order_id: str

    customer_id: str

    checkout_session_id: str

    checkout_url: str

    provider: str

    country: str

    plan: str

    interval: BillingInterval

    price: float

    currency: str