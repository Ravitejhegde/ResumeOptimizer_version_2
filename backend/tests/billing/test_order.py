from app.database.models.order import Order


def test_order_is_paid():
    order = Order(status="completed")

    assert order.is_paid is True


def test_order_is_not_paid():
    order = Order(status="pending")

    assert order.is_paid is False