from pydantic import BaseModel


class PricingResponse(BaseModel):
    """
    Pricing information exposed to the frontend.
    """

    id: str

    plan_code: str

    plan_name: str

    description: str | None = None

    country_code: str

    currency_code: str

    monthly_price: float

    yearly_price: float | None = None

    monthly_optimizations: int

    payment_provider: str

    active: bool