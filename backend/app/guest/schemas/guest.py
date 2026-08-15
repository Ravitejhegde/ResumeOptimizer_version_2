from pydantic import BaseModel, Field


class GuestSessionRequest(BaseModel):
    """
    Request to create a guest session.

    referral_code is optional because a normal visitor
    may enter the application without a referral.
    """

    browser_id: str = Field(
        min_length=1,
        max_length=120,
    )

    country: str = Field(
        default="IN",
        min_length=2,
        max_length=5,
    )

    language: str = Field(
        default="en",
        min_length=2,
        max_length=10,
    )

    referral_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )


class GuestSessionResponse(BaseModel):
    """
    Guest session returned to the client.
    """

    guest_id: str

    session_token: str

    country: str

    language: str