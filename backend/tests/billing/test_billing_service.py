from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.billing.services.billing_service import (
    BillingService,
)


def build_service():
    service = BillingService.__new__(
        BillingService
    )

    service._providers = {}

    return service


def test_provider_returns_registered_provider():
    service = build_service()

    provider = Mock()
    service._providers["stripe"] = provider

    result = service.provider("stripe")

    assert result is provider


def test_provider_uses_settings_when_not_provided():
    service = build_service()

    provider = Mock()
    service._providers["stripe"] = provider

    with patch(
        "app.billing.services.billing_service.settings.BILLING_PROVIDER",
        "stripe",
    ):
        result = service.provider()

    assert result is provider


def test_provider_normalizes_provider_name():
    service = build_service()

    provider = Mock()
    service._providers["stripe"] = provider

    result = service.provider("  STRIPE  ")

    assert result is provider


def test_provider_raises_for_unsupported_provider():
    service = build_service()

    with pytest.raises(
        ValueError,
        match="Unsupported payment provider: paypal",
    ):
        service.provider("paypal")


@pytest.mark.asyncio
async def test_create_customer():
    service = build_service()

    provider = Mock()
    provider.create_customer = AsyncMock(
        return_value="cus_123"
    )

    service._providers["stripe"] = provider

    result = await service.create_customer(
        email="test@example.com",
        name="Test User",
        provider="stripe",
    )

    assert result == "cus_123"

    provider.create_customer.assert_awaited_once_with(
        email="test@example.com",
        name="Test User",
    )


@pytest.mark.asyncio
async def test_create_checkout_session():
    service = build_service()

    provider = Mock()

    provider.create_checkout_session = AsyncMock(
        return_value={
            "id": "cs_123",
            "url": "https://checkout.example.com",
        }
    )

    service._providers["stripe"] = provider

    result = await service.create_checkout_session(
        customer_id="cus_123",
        price_id="price_123",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        client_reference_id="order_123",
        metadata={
            "order_id": "order_123",
        },
        allow_promotion_codes=True,
        automatic_tax=True,
        provider="stripe",
    )

    assert result == {
        "id": "cs_123",
        "url": "https://checkout.example.com",
    }

    provider.create_checkout_session.assert_awaited_once_with(
        customer_id="cus_123",
        price_id="price_123",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        client_reference_id="order_123",
        metadata={
            "order_id": "order_123",
        },
        allow_promotion_codes=True,
        automatic_tax=True,
    )


@pytest.mark.asyncio
async def test_create_billing_portal():
    service = build_service()

    provider = Mock()

    provider.create_billing_portal = AsyncMock(
        return_value="https://billing.example.com",
    )

    service._providers["stripe"] = provider

    result = await service.create_billing_portal(
        customer_id="cus_123",
        return_url="https://example.com/account",
        provider="stripe",
    )

    assert result == "https://billing.example.com"

    provider.create_billing_portal.assert_awaited_once_with(
        customer_id="cus_123",
        return_url="https://example.com/account",
    )


@pytest.mark.asyncio
async def test_get_subscription():
    service = build_service()

    provider = Mock()

    provider.get_subscription = AsyncMock(
        return_value={
            "id": "sub_123",
            "status": "active",
        }
    )

    service._providers["stripe"] = provider

    result = await service.get_subscription(
        subscription_id="sub_123",
        provider="stripe",
    )

    assert result["id"] == "sub_123"
    assert result["status"] == "active"

    provider.get_subscription.assert_awaited_once_with(
        subscription_id="sub_123",
    )


@pytest.mark.asyncio
async def test_cancel_subscription():
    service = build_service()

    provider = Mock()
    provider.cancel_subscription = AsyncMock()

    service._providers["stripe"] = provider

    result = await service.cancel_subscription(
        subscription_id="sub_123",
        provider="stripe",
    )

    assert result is None

    provider.cancel_subscription.assert_awaited_once_with(
        subscription_id="sub_123",
    )


@pytest.mark.asyncio
async def test_verify_webhook():
    service = build_service()

    provider = Mock()

    provider.verify_webhook = AsyncMock(
        return_value={
            "id": "evt_123",
            "type": "checkout.session.completed",
        }
    )

    service._providers["stripe"] = provider

    payload = b'{"id":"evt_123"}'

    result = await service.verify_webhook(
        payload=payload,
        signature="signature_123",
        provider="stripe",
    )

    assert result["id"] == "evt_123"

    provider.verify_webhook.assert_awaited_once_with(
        payload=payload,
        signature="signature_123",
    )


@pytest.mark.asyncio
async def test_create_refund():
    service = build_service()

    provider = Mock()

    provider.create_refund = AsyncMock(
        return_value={
            "id": "re_123",
            "status": "succeeded",
        }
    )

    service._providers["stripe"] = provider

    result = await service.create_refund(
        payment_id="pi_123",
        provider="stripe",
    )

    assert result["id"] == "re_123"
    assert result["status"] == "succeeded"

    provider.create_refund.assert_awaited_once_with(
        payment_id="pi_123",
    )