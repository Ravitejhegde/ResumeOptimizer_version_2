from __future__ import annotations

from pydantic import BaseModel, Field


class ReferralLinkResponse(BaseModel):
    """
    Referral link belonging to the current guest.
    """

    referral_code: str

    referral_url: str


class ReferralCreateRequest(BaseModel):
    """
    Data received when a guest arrives through
    another guest's referral link.
    """

    referral_code: str = Field(
        min_length=1,
        max_length=100,
    )


class ReferralCreateResponse(BaseModel):
    """
    Result of creating a referral relationship.
    """

    success: bool

    message: str


class ReferralStatsResponse(BaseModel):
    """
    Referral statistics for a guest.
    """

    total_referrals: int

    rewarded_referrals: int

    pending_rewards: int

    earned_samples: int