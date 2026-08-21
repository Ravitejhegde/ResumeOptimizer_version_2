import pytest

from app.billing.services.checkout_service import CheckoutService


@pytest.mark.asyncio
async def test_create_checkout_rejects_invalid_interval(db_session):
    service = CheckoutService(db_session)

    with pytest.raises(
        ValueError,
        match="Invalid billing interval",
    ):
        await service.create_checkout(
            user_id="user-1",
            email="test@example.com",
            name="Test User",
            plan_code="pro",
            country="IN",
            interval="weekly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
@pytest.mark.asyncio
async def test_create_checkout_rejects_missing_pricing(db_session):
    service = CheckoutService(db_session)

    with pytest.raises(
        ValueError,
        match="Pricing not found",
    ):
        await service.create_checkout(
            user_id="user-1",
            email="test@example.com",
            name="Test User",
            plan_code="nonexistent-plan",
            country="IN",
            interval="monthly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

@pytest.mark.asyncio
async def test_create_checkout_rejects_provider_mismatch(db_session):
    from app.database.models.plan import Plan
    from app.database.models.pricing import Pricing

    plan = Plan(
        code="pro",
        name="Pro",
        active=True,
    )

    db_session.add(plan)
    db_session.flush()

    pricing = Pricing(
        plan_id=plan.id,
        country_code="IN",
        currency_code="INR",
        monthly_price=499,
        yearly_price=4999,
        payment_provider="razorpay",
        stripe_monthly_price_id="price_monthly_test",
        stripe_yearly_price_id="price_yearly_test",
        active=True,
    )

    db_session.add(pricing)
    db_session.commit()

    service = CheckoutService(db_session)

    with pytest.raises(
        ValueError,
        match="payment provider is not configured",
    ):
        await service.create_checkout(
            user_id="user-1",
            email="test@example.com",
            name="Test User",
            plan_code="pro",
            country="IN",
            interval="monthly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            provider="stripe",
        )
@pytest.mark.asyncio
async def test_create_checkout_rejects_missing_yearly_price(db_session):
    from app.database.models.plan import Plan
    from app.database.models.pricing import Pricing

    plan = Plan(
        code="basic",
        name="Basic",
        active=True,
    )

    db_session.add(plan)
    db_session.flush()

    pricing = Pricing(
        plan_id=plan.id,
        country_code="IN",
        currency_code="INR",
        monthly_price=299,
        yearly_price=None,
        payment_provider="stripe",
        stripe_monthly_price_id="price_monthly_test",
        stripe_yearly_price_id=None,
        active=True,
    )

    db_session.add(pricing)
    db_session.commit()

    service = CheckoutService(db_session)

    with pytest.raises(
        ValueError,
        match="Yearly pricing is not available",
    ):
        await service.create_checkout(
            user_id="user-1",
            email="test@example.com",
            name="Test User",
            plan_code="basic",
            country="IN",
            interval="yearly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            provider="stripe",
        )
@pytest.mark.asyncio
async def test_create_checkout_rejects_missing_stripe_price_id(db_session):
    from app.database.models.plan import Plan
    from app.database.models.pricing import Pricing

    plan = Plan(
        code="starter",
        name="Starter",
        active=True,
    )

    db_session.add(plan)
    db_session.flush()

    pricing = Pricing(
        plan_id=plan.id,
        country_code="IN",
        currency_code="INR",
        monthly_price=199,
        yearly_price=1999,
        payment_provider="stripe",
        stripe_monthly_price_id=None,
        stripe_yearly_price_id="price_yearly_test",
        active=True,
    )

    db_session.add(pricing)
    db_session.commit()

    service = CheckoutService(db_session)

    with pytest.raises(
        ValueError,
        match="No monthly Stripe price",
    ):
        await service.create_checkout(
            user_id="user-1",
            email="test@example.com",
            name="Test User",
            plan_code="starter",
            country="IN",
            interval="monthly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            provider="stripe",
        )