from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


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

    interval: str = Field(
        default="monthly",
        pattern="^(monthly|yearly)$",
    )

    provider: str = Field(
        default="stripe",
    )

    success_url: str

    cancel_url: str


class CheckoutResponse(BaseModel):
    """
    Checkout response.
    """

    customer_id: str

    checkout_session_id: str

    checkout_url: str

    provider: str

    country: str

    plan: str

    interval: str

    price: float

    currency: str

    trial_days: int

    features: list[str]