from __future__ import annotations

import uuid

from app.database.models.email_verification_token import (
    EmailVerificationToken,
)
from app.services.auth.auth_service import AuthService
from app.services.auth.email_verification_service import (
    EmailVerificationService,
)


def test_email_verification_marks_user_verified_and_consumes_otp(
    db,
    monkeypatch,
):
    email = f"verify_{uuid.uuid4().hex[:8]}@example.com"

    monkeypatch.setattr(
        "app.services.auth.auth_service.EmailVerificationService.send_verification_email",
        lambda self, user, raw_token: None,
    )

    service = AuthService(db)

    user = service.register(
        email=email,
        password="TestPassword123!",
        name="Verification Test",
    )

    verification_service = EmailVerificationService(db)

    raw_otp = verification_service.create_verification_token(
        user
    )

    token_hash = verification_service._hash_token(
        raw_otp
    )

    verification_service.verify_email_for_user(
        email=email,
        raw_token=raw_otp,
    )

    db.refresh(user)

    assert user.verified is True

    used_token = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.token_hash == token_hash,
        )
        .first()
    )

    assert used_token is not None
    assert used_token.used is True
    assert used_token.is_valid is False

    # OTP must not be reusable.
    try:
        verification_service.verify_email_for_user(
            email=email,
            raw_token=raw_otp,
        )
        assert False, "OTP reuse should have been rejected."
    except ValueError as exc:
        assert str(exc) == "Email is already verified."

    db.delete(user)
    db.commit()