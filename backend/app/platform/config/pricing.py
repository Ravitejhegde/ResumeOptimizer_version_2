from dataclasses import dataclass


@dataclass(frozen=True)
class Pricing:

    monthly: float

    yearly: float

    currency: str


PRICING = {

    "IN": Pricing(
        monthly=49,
        yearly=299,
        currency="INR",
    ),

    "US": Pricing(
        monthly=4.99,
        yearly=39.99,
        currency="USD",
    ),

    "GB": Pricing(
        monthly=3.99,
        yearly=34.99,
        currency="GBP",
    ),
}