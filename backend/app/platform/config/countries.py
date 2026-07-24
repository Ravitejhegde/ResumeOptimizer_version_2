from dataclasses import dataclass


@dataclass(frozen=True)
class Country:

    code: str

    name: str

    currency: str

    payment_provider: str

    language: str


COUNTRIES = {

    "IN": Country(
        code="IN",
        name="India",
        currency="INR",
        payment_provider="razorpay",
        language="en",
    ),

    "US": Country(
        code="US",
        name="United States",
        currency="USD",
        payment_provider="stripe",
        language="en",
    ),

    "GB": Country(
        code="GB",
        name="United Kingdom",
        currency="GBP",
        payment_provider="stripe",
        language="en",
    ),
}