from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest

from app.billing.services.subscription_service import (
    SubscriptionService,
)


def build_service():
    service = SubscriptionService.__new__(
        SubscriptionService
    )

    service.subscriptions = Mock()
    service.billing = Mock()

    return service


@pytest.mark.asyncio
async def test_get_remote_subscription():
    service = build_service()

    service.billing.get_subscription = AsyncMock(
        return_value={
            "id": "sub_123",
            "status": "active",
        }
    )

    result = await service.get_remote_subscription(
        "sub_123"
    )

    assert result["id"] == "sub_123"

    service.billing.get_subscription.assert_awaited_once_with(
        subscription_id="sub_123"
    )


@pytest.mark.asyncio
async def test_cancel_remote_subscription():
    service = build_service()

    service.billing.cancel_subscription = AsyncMock()

    await service.cancel_remote_subscription(
        "sub_123"
    )

    service.billing.cancel_subscription.assert_awaited_once_with(
        subscription_id="sub_123"
    )


def test_get_user_subscription():
    service = build_service()

    subscription = Mock()

    service.subscriptions.get_active.return_value = (
        subscription
    )

    result = service.get_user_subscription(
        "user_123"
    )

    assert result is subscription

    service.subscriptions.get_active.assert_called_once_with(
        "user_123"
    )


def test_cancel_local_subscription():
    service = build_service()

    subscription = Mock()

    service.subscriptions.update.return_value = (
        subscription
    )

    result = service.cancel_local_subscription(
        subscription
    )

    assert result is subscription
    assert subscription.status == "cancelled"

    assert isinstance(
        subscription.cancelled_at,
        datetime,
    )

    assert subscription.cancelled_at.tzinfo == timezone.utc

    service.subscriptions.update.assert_called_once_with(
        subscription
    )


@pytest.mark.asyncio
async def test_status_returns_provider_status():
    service = build_service()

    service.billing.get_subscription = AsyncMock(
        return_value={
            "status": "active",
        }
    )

    result = await service.status(
        "sub_123"
    )

    assert result == "active"


@pytest.mark.asyncio
async def test_status_returns_unknown_when_missing():
    service = build_service()

    service.billing.get_subscription = AsyncMock(
        return_value={}
    )

    result = await service.status(
        "sub_123"
    )

    assert result == "unknown"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "provider_status, expected",
    [
        ("active", True),
        ("trialing", True),
        ("cancelled", False),
        ("past_due", False),
        ("unknown", False),
    ],
)
async def test_is_active(
    provider_status,
    expected,
):
    service = build_service()

    service.status = AsyncMock(
        return_value=provider_status
    )

    result = await service.is_active(
        "sub_123"
    )

    assert result is expected


@pytest.mark.asyncio
async def test_period():
    service = build_service()

    service.billing.get_subscription = AsyncMock(
        return_value={
            "current_period_start": 1000,
            "current_period_end": 2000,
        }
    )

    result = await service.period(
        "sub_123"
    )

    assert result == {
        "start": 1000,
        "end": 2000,
    }


@pytest.mark.asyncio
async def test_sync_status():
    service = build_service()

    service.billing.get_subscription = AsyncMock(
        return_value={
            "status": "active",
            "current_period_start": 1000,
            "current_period_end": 2000,
        }
    )

    subscription = Mock()

    service.subscriptions.update.return_value = (
        subscription
    )

    result = await service.sync_status(
        "sub_123",
        subscription,
    )

    assert result is subscription
    assert subscription.status == "active"

    assert subscription.expires_at == datetime.fromtimestamp(
        2000,
        tz=timezone.utc,
    )

    service.subscriptions.update.assert_called_once_with(
        subscription
    )