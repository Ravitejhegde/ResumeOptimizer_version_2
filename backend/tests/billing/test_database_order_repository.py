from decimal import Decimal

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)
from app.database.models.order import Order


def test_create_and_get_order(db_session):
    repository = DatabaseOrderRepository(db_session)

    order = Order(
        user_id="user-1",
        pricing_id="pricing-1",
        provider="stripe",
        amount=Decimal("99.00"),
        currency="INR",
        status="pending",
    )

    created = repository.create(order)
    db_session.commit()

    assert created.id is not None

    fetched = repository.get(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.user_id == "user-1"
    assert fetched.status == "pending"


def test_get_by_provider_order_id(db_session):
    repository = DatabaseOrderRepository(db_session)

    order = Order(
        user_id="user-2",
        pricing_id="pricing-2",
        provider="stripe",
        amount=Decimal("199.00"),
        currency="INR",
        status="pending",
        provider_order_id="cs_test_123",
    )

    repository.create(order)
    db_session.commit()

    fetched = repository.get_by_provider_order_id(
        "cs_test_123"
    )

    assert fetched is not None
    assert fetched.id == order.id
    assert fetched.provider_order_id == "cs_test_123"