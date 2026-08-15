from __future__ import annotations

from pydantic import BaseModel, Field


class ReferralLinkResponse(BaseModel):
    referral_code: str = Field(
        min_length=1,
        max_length=64,
    )

    referral_url: str


ReferralCodeResponse = ReferralLinkResponse


class ReferralCreateRequest(BaseModel):
    referral_code: str = Field(
        min_length=1,
        max_length=64,
    )


class ReferralCreateResponse(BaseModel):
    success: bool
    message: str


class ReferralResponse(BaseModel):
    id: str
    status: str
    reward_granted: bool
    created_at: str
    rewarded_at: str | None = None


class ReferralStatsResponse(BaseModel):
    total_referrals: int
    rewarded_referrals: int
    pending_rewards: int
    earned_samples: int


class ReferralSummaryResponse(BaseModel):
    referral_code: str
    total_referrals: int
    rewarded_referrals: int
    pending_referrals: int
    earned_samples: int