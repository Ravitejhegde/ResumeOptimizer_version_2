"""
Email verification service.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.models.email_verification_token import (
    EmailVerificationToken,
)
from app.database.models.user import User
from app.database.repositories.email_verification_token_repository import (
    EmailVerificationTokenRepository,
)
from app.database.repositories.user_repository import (
    UserRepository,
)
from app.services.email.email_service import EmailService


class EmailVerificationService:
    """
    Handles email verification business logic.

    Responsibilities:
        - Generate six-digit verification OTPs.
        - Store only OTP hashes.
        - Send verification emails.
        - Validate verification OTPs.
        - Mark users as verified.
        - Mark verification tokens as used.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.users = UserRepository(db)

        self.tokens = EmailVerificationTokenRepository(
            db
        )

        self.email = EmailService()

    # ==========================================================
    # Token Generation
    # ==========================================================

    def create_verification_token(
        self,
        user: User,
    ) -> str:
        """
        Create a new six-digit email verification OTP.

        Returns:
            Raw six-digit OTP that can be sent to the user.

        Important:
            The raw OTP is never stored in the database.
            Only its SHA-256 hash is stored.
        """

        raw_token = (
            f"{secrets.randbelow(1_000_000):06d}"
        )

        token_hash = self._hash_token(
            raw_token
        )

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS
            )
        )

        token = EmailVerificationToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.tokens.create(
            token
        )

        return raw_token

    # ==========================================================
    # Send Verification Email
    # ==========================================================

    def send_verification_email(
        self,
        user: User,
        raw_token: str,
    ) -> None:
        """
        Send the six-digit verification OTP by email.
        """

        subject = (
            "Your ResumeOptimizer verification code"
        )

        body = f"""
Hello {user.name},

Welcome to ResumeOptimizer.

Your email verification code is:

{raw_token}

Enter this code in ResumeOptimizer to verify your email address.

This code expires in
{settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours.

If you did not create this account, you can safely ignore this email.

Regards,
ResumeOptimizer
""".strip()

        self.email.send_email(
            to_email=user.email,
            subject=subject,
            body=body,
        )

        # ==========================================================
    # Verification With Email
    # ==========================================================

    def verify_email_for_user(
        self,
        email: str,
        raw_token: str,
    ) -> User:
        """
        Verify a user's email using their email address
        and six-digit verification OTP.
        """

        user = self.users.get_by_email(
            email
        )

        if user is None:
            raise ValueError(
                "Invalid email or verification code."
            )

        if user.verified:
            raise ValueError(
                "Email is already verified."
            )

        token_hash = self._hash_token(
            raw_token
        )

        token = (
            self.tokens.get_by_token_hash(
                token_hash
            )
        )

        if token is None:
            raise ValueError(
                "Invalid email or verification code."
            )

        if token.user_id != user.id:
            raise ValueError(
                "Invalid email or verification code."
            )

        if not token.is_valid:
            raise ValueError(
                "Verification code is expired or already used."
            )

        user.verified = True

        self.users.update(
            user
        )

        self.tokens.mark_used(
            token
        )

        return user
    # ==========================================================
    # Verification
    # ==========================================================

    def verify_email(
        self,
        raw_token: str,
    ) -> User:
        """
        Verify a user's email using the six-digit OTP.
        """

        token_hash = self._hash_token(
            raw_token
        )

        token = (
            self.tokens.get_by_token_hash(
                token_hash
            )
        )

        if token is None:
            raise ValueError(
                "Invalid verification code."
            )

        if not token.is_valid:
            raise ValueError(
                "Verification code is expired or already used."
            )

        user = self.users.get(
            token.user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        if user.verified:
            raise ValueError(
                "Email is already verified."
            )

        user.verified = True

        self.users.update(
            user
        )

        self.tokens.mark_used(
            token
        )

        return user

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _hash_token(
        raw_token: str,
    ) -> str:
        """
        Hash the raw verification OTP.

        The raw OTP is never stored in the database.
        """

        return hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()