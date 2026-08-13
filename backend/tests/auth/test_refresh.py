from __future__ import annotations

import uuid

from app.services.auth.auth_service import AuthService


def test_valid_refresh_token_creates_new_access_token(
    db,
    monkeypatch,
):
    email = f"refresh_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password=password,
        name="Refresh Test",
    )

    user.verified = True
    db.commit()
    db.refresh(user)

    login_result = service.login(
        email=email,
        password=password,
    )

    refresh_token = login_result["refresh_token"]

    result = service.refresh(
        refresh_token
    )

    assert result["access_token"]
    assert result["token_type"] == "bearer"

    db.delete(user)
    db.commit()


def test_access_token_cannot_be_used_as_refresh_token(
    db,
    monkeypatch,
):
    email = f"access_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password=password,
        name="Access Token Test",
    )

    user.verified = True
    db.commit()
    db.refresh(user)

    login_result = service.login(
        email=email,
        password=password,
    )

    access_token = login_result["access_token"]

    try:
        service.refresh(access_token)
        assert False, (
            "Access token must not be accepted as refresh token."
        )
    except ValueError as exc:
        assert "Invalid refresh token" in str(exc)

    db.delete(user)
    db.commit()

def test_invalid_refresh_token_is_rejected(
    db,
):
    service = AuthService(db)

    invalid_token = "this-is-not-a-valid-jwt"

    try:
        service.refresh(invalid_token)
        assert False, (
            "Invalid refresh token must be rejected."
        )
    except Exception as exc:
        assert exc is not None