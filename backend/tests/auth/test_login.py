from __future__ import annotations

import uuid

import pytest

from app.services.auth.auth_service import AuthService


def test_unverified_user_cannot_login(
    db,
    monkeypatch,
):
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    # Prevent real email delivery.
    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password=password,
        name="Login Test",
    )

    assert user.verified is False

    with pytest.raises(
        ValueError,
        match="Please verify your email before logging in.",
    ):
        service.login(
            email=email,
            password=password,
        )

    db.delete(user)
    db.commit()


def test_verified_user_can_login(
    db,
    monkeypatch,
):
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    # Prevent real email delivery.
    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password=password,
        name="Verified Login Test",
    )

    # Simulate successful email verification.
    user.verified = True
    db.commit()
    db.refresh(user)

    result = service.login(
        email=email,
        password=password,
    )

    assert result["user"].id == user.id
    assert result["access_token"]
    assert result["refresh_token"]
    assert result["token_type"] == "bearer"

    db.delete(user)
    db.commit()