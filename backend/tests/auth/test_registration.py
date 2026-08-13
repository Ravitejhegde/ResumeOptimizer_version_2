from __future__ import annotations

import uuid

from app.database.models.email_verification_token import (
    EmailVerificationToken,
)
from app.services.auth.auth_service import AuthService


def test_register_creates_user_workspace_and_verification_token(
    db,
    monkeypatch,
):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    sent_email = {}

    def fake_send_verification_email(
        self,
        user,
        raw_token,
    ):
        sent_email["email"] = user.email
        sent_email["otp"] = raw_token

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        fake_send_verification_email,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password="TestPassword123!",
        name="Registration Test",
    )

    # ------------------------------------------------------
    # User
    # ------------------------------------------------------

    assert user.email == email
    assert user.verified is False
    assert user.active is True

    # ------------------------------------------------------
    # Workspace
    # ------------------------------------------------------

    db.refresh(user)

    assert user.workspace is not None
    assert user.workspace.user_id == user.id
    assert user.workspace.name == "My Workspace"

    # ------------------------------------------------------
    # Verification token
    # ------------------------------------------------------

    token = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.user_id == user.id
        )
        .first()
    )

    assert token is not None
    assert token.used is False
    assert token.is_valid is True

    # ------------------------------------------------------
    # Email verification call
    # ------------------------------------------------------

    assert sent_email["email"] == email
    assert len(sent_email["otp"]) == 6
    assert sent_email["otp"].isdigit()

    # The raw OTP must not be stored.
    assert token.token_hash != sent_email["otp"]
    assert len(token.token_hash) == 64

    # ------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------

    db.delete(user)
    db.commit()