from unittest.mock import Mock

import pytest

from app.billing.services.entitlement_service import (
    EntitlementService,
)


def build_service():
    service = EntitlementService.__new__(
        EntitlementService
    )

    service.db = Mock()

    return service


def test_feature_value_returns_none_when_no_subscription():
    service = build_service()

    (
        service.db.query.return_value
        .filter.return_value
        .first.return_value
    ) = None

    result = service.feature_value(
        "user_123",
        "resume_optimization",
    )

    assert result is None


def test_feature_value_returns_feature_value():
    service = build_service()

    subscription = Mock()
    order = Mock()
    pricing = Mock()
    plan = Mock()
    feature = Mock()
    plan_feature = Mock()

    subscription.order = order
    order.pricing = pricing
    pricing.plan = plan

    feature.id = "feature_123"
    plan.id = "plan_123"

    plan_feature.value = "100"

    (
        service.db.query.return_value
        .filter.return_value
        .first.side_effect
    ) = [
        subscription,
        feature,
        plan_feature,
    ]

    result = service.feature_value(
        "user_123",
        "resume_optimization",
    )

    assert result == "100"


def test_feature_value_returns_none_when_feature_missing():
    service = build_service()

    subscription = Mock()
    order = Mock()
    pricing = Mock()
    plan = Mock()

    subscription.order = order
    order.pricing = pricing
    pricing.plan = plan

    (
        service.db.query.return_value
        .filter.return_value
        .first.side_effect
    ) = [
        subscription,
        None,
    ]

    result = service.feature_value(
        "user_123",
        "resume_optimization",
    )

    assert result is None


def test_feature_value_returns_none_when_plan_feature_missing():
    service = build_service()

    subscription = Mock()
    order = Mock()
    pricing = Mock()
    plan = Mock()
    feature = Mock()

    subscription.order = order
    order.pricing = pricing
    pricing.plan = plan

    feature.id = "feature_123"
    plan.id = "plan_123"

    (
        service.db.query.return_value
        .filter.return_value
        .first.side_effect
    ) = [
        subscription,
        feature,
        None,
    ]

    result = service.feature_value(
        "user_123",
        "resume_optimization",
    )

    assert result is None


@pytest.mark.parametrize(
    "value, expected",
    [
        ("true", True),
        ("TRUE", True),
        ("True", True),
        ("false", False),
        ("FALSE", False),
        ("anything", False),
    ],
)
def test_has_feature(value, expected):
    service = build_service()

    service.feature_value = Mock(
        return_value=value
    )

    result = service.has_feature(
        "user_123",
        "resume_optimization",
    )

    assert result is expected


def test_has_feature_returns_false_when_missing():
    service = build_service()

    service.feature_value = Mock(
        return_value=None
    )

    result = service.has_feature(
        "user_123",
        "resume_optimization",
    )

    assert result is False


@pytest.mark.parametrize(
    "value, expected",
    [
        ("10", 10),
        ("100", 100),
        ("1", 1),
        ("0", 0),
    ],
)
def test_integer_limit(value, expected):
    service = build_service()

    service.feature_value = Mock(
        return_value=value
    )

    result = service.integer_limit(
        "user_123",
        "resume_optimization",
    )

    assert result == expected


def test_integer_limit_returns_none_when_missing():
    service = build_service()

    service.feature_value = Mock(
        return_value=None
    )

    result = service.integer_limit(
        "user_123",
        "resume_optimization",
    )

    assert result is None


def test_integer_limit_returns_none_for_unlimited():
    service = build_service()

    service.feature_value = Mock(
        return_value="unlimited"
    )

    result = service.integer_limit(
        "user_123",
        "resume_optimization",
    )

    assert result is None


def test_integer_limit_raises_for_invalid_value():
    service = build_service()

    service.feature_value = Mock(
        return_value="not-a-number"
    )

    with pytest.raises(ValueError):
        service.integer_limit(
            "user_123",
            "resume_optimization",
        )