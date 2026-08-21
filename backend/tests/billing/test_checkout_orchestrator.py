from unittest.mock import Mock

from app.billing.services.checkout_orchestrator import (
    CheckoutOrchestrator,
)
from app.database.models.order import Order


def build_service():
    service = CheckoutOrchestrator.__new__(
        CheckoutOrchestrator
    )

    service.db = Mock()
    service.orders = Mock()

    return service


def test_create_order():
    service = build_service()

    created_order = Mock(spec=Order)

    service.orders.create.return_value = (
        created_order
    )

    result = service.create_order(
        user_id="user_123",
        pricing_id="pricing_123",
        amount=99.0,
        currency="INR",
    )

    assert result is created_order

    service.orders.create.assert_called_once()

    order = (
        service.orders.create.call_args.args[0]
    )

    assert isinstance(order, Order)
    assert order.user_id == "user_123"
    assert order.pricing_id == "pricing_123"
    assert order.amount == 99.0
    assert order.currency == "INR"
    assert order.status == "pending"


def test_create_order_passes_order_to_repository():
    service = build_service()

    service.orders.create.return_value = (
        Mock(spec=Order)
    )

    service.create_order(
        user_id="user_456",
        pricing_id="pricing_456",
        amount=199.0,
        currency="USD",
    )

    service.orders.create.assert_called_once()

    order = (
        service.orders.create.call_args.args[0]
    )

    assert order.user_id == "user_456"
    assert order.pricing_id == "pricing_456"
    assert order.amount == 199.0
    assert order.currency == "USD"
    assert order.status == "pending"