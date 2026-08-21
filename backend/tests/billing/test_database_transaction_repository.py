from __future__ import annotations

from decimal import Decimal

from app.billing.repository.database_transaction_repository import (
    DatabaseTransactionRepository,
)
from app.database.models.order import Order
from app.database.models.plan import Plan
from app.database.models.pricing import Pricing
from app.database.models.payment_transaction import (
    PaymentTransaction,
)


def create_test_pricing(db_session):
    """
    Create the minimum valid Plan + Pricing records
    required by the Order model.
    """

    plan = Plan(
        code="test-plan",
        name="Test Plan",
        active=True,
    )

    db_session.add(plan)
    db_session.flush()

    pricing = Pricing(
        plan_id=plan.id,
        country_code="IN",
        currency_code="INR",
        monthly_price=Decimal("99.00"),
        yearly_price=Decimal("999.00"),
        payment_provider="stripe",
        stripe_monthly_price_id="price_monthly_test",
        stripe_yearly_price_id="price_yearly_test",
        active=True,
    )

    db_session.add(pricing)
    db_session.flush()

    return pricing


def create_test_order(db_session):
    """
    Create a valid Order with its required Pricing.
    """

    pricing = create_test_pricing(
        db_session
    )

    order = Order(
        user_id="test-user",
        pricing_id=pricing.id,
        amount=Decimal("99.00"),
        currency="INR",
        status="paid",
        provider="stripe",
    )

    db_session.add(order)
    db_session.flush()

    return order


def test_create_transaction(db_session):
    order = create_test_order(
        db_session
    )

    repository = DatabaseTransactionRepository(
        db_session
    )

    transaction = PaymentTransaction(
        order_id=order.id,
        provider="stripe",
        provider_transaction_id="txn_test_001",
        amount=Decimal("99.00"),
        currency="INR",
        status="paid",
    )

    result = repository.create(
        transaction
    )

    assert result.id is not None
    assert result.order_id == order.id
    assert result.provider == "stripe"
    assert (
        result.provider_transaction_id
        == "txn_test_001"
    )


def test_get_by_provider_transaction_id(
    db_session,
):
    order = create_test_order(
        db_session
    )

    transaction = PaymentTransaction(
        order_id=order.id,
        provider="stripe",
        provider_transaction_id="txn_test_002",
        amount=Decimal("99.00"),
        currency="INR",
        status="paid",
    )

    db_session.add(transaction)
    db_session.flush()

    repository = DatabaseTransactionRepository(
        db_session
    )

    result = (
        repository.get_by_provider_transaction_id(
            "txn_test_002"
        )
    )

    assert result is not None
    assert result.id == transaction.id
    assert (
        result.provider_transaction_id
        == "txn_test_002"
    )