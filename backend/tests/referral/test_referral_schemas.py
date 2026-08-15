from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.referral.schemas.referral import (
    ReferralCreateRequest,
    ReferralCreateResponse,
    ReferralLinkResponse,
    ReferralStatsResponse,
)


def test_referral_link_response():
    result = ReferralLinkResponse(
        referral_code="ABC123",
        referral_url="https://resumeoptimizer.app/r/ABC123",
    )

    assert result.referral_code == "ABC123"
    assert result.referral_url.endswith("ABC123")


def test_referral_create_request():
    result = ReferralCreateRequest(
        referral_code="ABC123",
    )

    assert result.referral_code == "ABC123"


def test_referral_create_request_rejects_empty_code():
    with pytest.raises(ValidationError):
        ReferralCreateRequest(
            referral_code="",
        )


def test_referral_create_response():
    result = ReferralCreateResponse(
        success=True,
        message="Referral created successfully.",
    )

    assert result.success is True
    assert result.message == "Referral created successfully."


def test_referral_stats_response():
    result = ReferralStatsResponse(
        total_referrals=5,
        rewarded_referrals=3,
        pending_rewards=2,
        earned_samples=6,
    )

    assert result.total_referrals == 5
    assert result.rewarded_referrals == 3
    assert result.pending_rewards == 2
    assert result.earned_samples == 6