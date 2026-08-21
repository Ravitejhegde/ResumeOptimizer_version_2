from unittest.mock import Mock

import pytest

from app.billing.services.usage_service import (
    UsageService,
)


def build_service():
    service = UsageService.__new__(
        UsageService
    )

    service.entitlements = Mock()

    return service


def test_limit_returns_integer_limit():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.limit(
        user_id="user_123",
        feature="resume_optimization",
    )

    assert result == 100

    service.entitlements.integer_limit.assert_called_once_with(
        "user_123",
        "resume_optimization",
    )


def test_limit_returns_none_for_unlimited():
    service = build_service()

    service.entitlements.integer_limit.return_value = None

    result = service.limit(
        user_id="user_123",
        feature="resume_optimization",
    )

    assert result is None


def test_unlimited_returns_true():
    service = build_service()

    service.entitlements.integer_limit.return_value = None

    result = service.unlimited(
        user_id="user_123",
        feature="resume_optimization",
    )

    assert result is True


def test_unlimited_returns_false():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.unlimited(
        user_id="user_123",
        feature="resume_optimization",
    )

    assert result is False


def test_can_use_when_under_limit():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.can_use(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=50,
    )

    assert result is True


def test_can_use_when_at_limit():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.can_use(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=100,
    )

    assert result is False


def test_can_use_when_over_limit():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.can_use(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=101,
    )

    assert result is False


def test_can_use_when_unlimited():
    service = build_service()

    service.entitlements.integer_limit.return_value = None

    result = service.can_use(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=999999,
    )

    assert result is True


def test_remaining_returns_remaining_usage():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.remaining(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=40,
    )

    assert result == 60


def test_remaining_never_goes_below_zero():
    service = build_service()

    service.entitlements.integer_limit.return_value = 100

    result = service.remaining(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=150,
    )

    assert result == 0


def test_remaining_returns_none_when_unlimited():
    service = build_service()

    service.entitlements.integer_limit.return_value = None

    result = service.remaining(
        user_id="user_123",
        feature="resume_optimization",
        current_usage=150,
    )

    assert result is None


def test_usage_summary():
    service = build_service()

    service.entitlements.integer_limit.side_effect = [
        100,
        None,
    ]

    result = service.usage_summary(
        user_id="user_123",
        usage={
            "resume_optimization": 25,
            "other_feature": 10,
        },
    )

    assert result == {
        "resume_optimization": {
            "used": 25,
            "limit": 100,
            "remaining": 75,
            "unlimited": False,
            "allowed": True,
        },
        "other_feature": {
            "used": 10,
            "limit": None,
            "remaining": None,
            "unlimited": True,
            "allowed": True,
        },
    }