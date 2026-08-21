from datetime import datetime, timedelta, timezone

from app.database.models.subscription import Subscription


def test_subscription_is_active_when_not_expired():
    now = datetime.now(timezone.utc)

    subscription = Subscription(
        user_id="user-1",
        order_id="order-1",
        status="active",
        starts_at=now,
        expires_at=now + timedelta(days=30),
    )

    assert subscription.is_active is True


def test_subscription_is_not_active_when_expired():
    now = datetime.now(timezone.utc)

    subscription = Subscription(
        user_id="user-1",
        order_id="order-1",
        status="active",
        starts_at=now - timedelta(days=60),
        expires_at=now - timedelta(days=1),
    )

    assert subscription.is_active is False