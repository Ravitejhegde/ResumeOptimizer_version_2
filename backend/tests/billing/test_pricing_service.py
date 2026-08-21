from decimal import Decimal

import pytest

from app.billing.services.pricing_service import PricingService
from app.database.models.feature import Feature
from app.database.models.plan import Plan
from app.database.models.plan_feature import PlanFeature
from app.database.models.pricing import Pricing


def create_plan_with_feature(
    db_session,
    *,
    plan_code="pro",
    plan_name="Pro",
    feature_code="resume_optimization",
    feature_value="100",
):
    plan = Plan(
        code=plan_code,
        name=plan_name,
        description="Pro plan",
        active=True,
    )

    feature = Feature(
        code=feature_code,
        name="Resume Optimization",
        description="Monthly resume optimizations",
        value_type="integer",
        active=True,
    )

    db_session.add(plan)
    db_session.add(feature)
    db_session.flush()

    plan_feature = PlanFeature(
        plan_id=plan.id,
        feature_id=feature.id,
        value=feature_value,
        active=True,
    )

    db_session.add(plan_feature)
    db_session.flush()

    return plan, feature, plan_feature


def create_pricing(
    db_session,
    plan,
    *,
    country_code="IN",
    currency_code="INR",
    monthly_price=499,
    yearly_price=4999,
    payment_provider="stripe",
    active=True,
):
    pricing = Pricing(
        plan_id=plan.id,
        country_code=country_code,
        currency_code=currency_code,
        monthly_price=Decimal(str(monthly_price)),
        yearly_price=(
            Decimal(str(yearly_price))
            if yearly_price is not None
            else None
        ),
        payment_provider=payment_provider,
        stripe_monthly_price_id="price_monthly_test",
        stripe_yearly_price_id="price_yearly_test",
        active=active,
    )

    db_session.add(pricing)
    db_session.commit()

    return pricing


def test_by_country_returns_pricing_response(db_session):
    plan, _, _ = create_plan_with_feature(
        db_session,
        plan_code="pro",
        plan_name="Pro",
        feature_value="100",
    )

    pricing = create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    result = service.by_country("IN")

    assert len(result) == 1

    item = result[0]

    assert item["id"] == pricing.id
    assert item["plan_code"] == "pro"
    assert item["plan_name"] == "Pro"
    assert item["plan_description"] == "Pro plan"
    assert item["country_code"] == "IN"
    assert item["currency_code"] == "INR"
    assert item["monthly_price"] == 499.0
    assert item["yearly_price"] == 4999.0
    assert item["monthly_optimizations"] == 100
    assert item["payment_provider"] == "stripe"
    assert item["active"] is True


def test_get_returns_pricing_response(db_session):
    plan, _, _ = create_plan_with_feature(
        db_session,
        plan_code="pro",
        plan_name="Pro",
        feature_value="250",
    )

    create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    result = service.get(
        plan_code="pro",
        country="IN",
    )

    assert result is not None
    assert result["plan_code"] == "pro"
    assert result["monthly_optimizations"] == 250


def test_get_returns_none_when_pricing_missing(db_session):
    service = PricingService(db_session)

    result = service.get(
        plan_code="nonexistent",
        country="IN",
    )

    assert result is None


def test_build_response_converts_decimal_prices(db_session):
    plan, _, _ = create_plan_with_feature(
        db_session,
        feature_value="50",
    )

    pricing = create_pricing(
        db_session,
        plan,
        monthly_price="299.50",
        yearly_price="2999.00",
    )

    service = PricingService(db_session)

    result = service._build_response(pricing)

    assert result["monthly_price"] == 299.50
    assert result["yearly_price"] == 2999.0
    assert result["monthly_optimizations"] == 50


def test_build_response_supports_missing_yearly_price(db_session):
    plan, _, _ = create_plan_with_feature(
        db_session,
        feature_value="10",
    )

    pricing = create_pricing(
        db_session,
        plan,
        yearly_price=None,
    )

    service = PricingService(db_session)

    result = service._build_response(pricing)

    assert result["yearly_price"] is None


def test_build_response_raises_when_feature_missing(db_session):
    plan = Plan(
        code="pro",
        name="Pro",
        description="Pro plan",
        active=True,
    )

    db_session.add(plan)
    db_session.flush()

    pricing = create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    with pytest.raises(
        ValueError,
        match="Resume optimization limit is not configured",
    ):
        service._build_response(pricing)


def test_build_response_raises_when_feature_inactive(db_session):
    plan, feature, _ = create_plan_with_feature(
        db_session,
        feature_value="100",
    )

    feature.active = False
    db_session.flush()

    pricing = create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    with pytest.raises(
        ValueError,
        match="Resume optimization limit is not configured",
    ):
        service._build_response(pricing)


def test_build_response_raises_when_plan_feature_inactive(db_session):
    plan, _, plan_feature = create_plan_with_feature(
        db_session,
        feature_value="100",
    )

    plan_feature.active = False
    db_session.flush()

    pricing = create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    with pytest.raises(
        ValueError,
        match="Resume optimization limit is not configured",
    ):
        service._build_response(pricing)


def test_build_response_raises_when_feature_value_is_invalid(db_session):
    plan, _, _ = create_plan_with_feature(
        db_session,
        feature_value="not-a-number",
    )

    pricing = create_pricing(
        db_session,
        plan,
    )

    service = PricingService(db_session)

    with pytest.raises(
        ValueError,
        match="Invalid resume optimization limit",
    ):
        service._build_response(pricing)