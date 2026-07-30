from pydantic import BaseModel, ConfigDict


class PricingResponse(BaseModel):
    """
    Country-specific pricing.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    country_code: str

    currency_code: str

    monthly_price: float

    yearly_price: float | None

    payment_provider: str

    active: bool




