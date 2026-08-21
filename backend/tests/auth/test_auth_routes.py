from __future__ import annotations

import uuid

from app.database.models.user import User


def unique_email() -> str:
    return f"api_{uuid.uuid4().hex[:10]}@example.com"


# ==========================================================
# Register
# ==========================================================


def test_register_route(
    client,
    monkeypatch,
):
    email = unique_email()

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "API Test User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["verified"] is False
    assert "message" in data


def test_register_duplicate_email(
    client,
    monkeypatch,
):
    email = unique_email()

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    first = client.post(
        "/auth/register",
        json={
            "name": "First User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/auth/register",
        json={
            "name": "Second User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert second.status_code == 400


# ==========================================================
# Email Verification
# ==========================================================


def test_verify_email_route(
    client,
    db,
    monkeypatch,
):
    email = unique_email()

    sent = {}

    def fake_send(
        self,
        user,
        raw_token,
    ):
        sent["otp"] = raw_token

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        fake_send,
    )

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Verification User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201
    assert "otp" in sent

    response = client.post(
        "/auth/verify-email",
        json={
            "email": email,
            "otp": sent["otp"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert data["verified"] is True


def test_verify_email_invalid_otp(
    client,
    monkeypatch,
):
    email = unique_email()

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Invalid OTP User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/verify-email",
        json={
            "email": email,
            "otp": "000000",
        },
    )

    assert response.status_code == 400


# ==========================================================
# Login
# ==========================================================


def test_login_route(
    client,
    db,
    monkeypatch,
):
    email = unique_email()
    password = "TestPassword123!"

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Login API User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # ------------------------------------------------------
    # Use the SAME isolated test database used by the client.
    # ------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    assert user is not None

    user.verified = True

    db.commit()
    db.refresh(user)

    # ------------------------------------------------------
    # Login
    # ------------------------------------------------------

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_login_unverified_user(
    client,
    monkeypatch,
):
    email = unique_email()

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Unverified User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401


def test_login_wrong_password(
    client,
    db,
    monkeypatch,
):
    email = unique_email()

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Wrong Password User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    # ------------------------------------------------------
    # Use the SAME isolated test database.
    # ------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    assert user is not None

    user.verified = True

    db.commit()
    db.refresh(user)

    # ------------------------------------------------------
    # Wrong password
    # ------------------------------------------------------

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


# ==========================================================
# OAuth2 / Swagger Token
# ==========================================================


def test_oauth_token_route(
    client,
    db,
    monkeypatch,
):
    email = unique_email()
    password = "TestPassword123!"

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "OAuth User",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    # ------------------------------------------------------
    # Use the SAME isolated test database.
    # ------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    assert user is not None

    user.verified = True

    db.commit()
    db.refresh(user)

    # ------------------------------------------------------
    # OAuth2 login
    # ------------------------------------------------------

    response = client.post(
        "/auth/token",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"