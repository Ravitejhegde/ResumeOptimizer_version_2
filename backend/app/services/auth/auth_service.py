from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.security.jwt import jwt_service
from app.core.security.password import (
    hash_password,
    verify_password,
)

from app.database.models.user import User

from app.database.repositories.user_repository import (
    UserRepository,
)

from app.services.auth.email_verification_service import (
    EmailVerificationService,
)

from app.services.workspace.workspace_service import (
    WorkspaceService,
)


logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication business logic.

    Handles:
        - User registration
        - User login
        - Token refresh
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.users = UserRepository(db)

        self.workspace = WorkspaceService(
            db
        )

        self.email_verification = (
            EmailVerificationService(
                db
            )
        )

    # ==========================================================
    # Register
    # ==========================================================

    def register(
        self,
        email: str,
        password: str,
        name: str,
    ) -> User:
        """
        Create a new user account.

        New accounts remain unverified until the
        email verification process is completed.
        """

        existing = self.users.get_by_email(
            email
        )

        if existing:
            raise ValueError(
                "Email already registered."
            )

        hashed_password = hash_password(
            password
        )

        user = User(
            id=str(
                uuid.uuid4()
            ),
            email=email,
            password_hash=hashed_password,
            name=name,
            provider="email",
            country="IN",
            language="en",
            active=True,
            verified=False,
        )

        user = self.users.create(
            user
        )

        # ------------------------------------------------------
        # Create default workspace
        # ------------------------------------------------------

        self.workspace.create_workspace(
            user_id=user.id
        )

        # ------------------------------------------------------
        # Create email verification token
        # ------------------------------------------------------

        raw_token = (
            self.email_verification.create_verification_token(
                user
            )
        )

        # ------------------------------------------------------
        # Send verification email
        # ------------------------------------------------------

        self.email_verification.send_verification_email(
            user,
            raw_token,
        )

        logger.info(
            "User registered: %s",
            user.email,
        )

        return user

    # ==========================================================
    # Login
    # ==========================================================

    def login(
        self,
        email: str,
        password: str,
    ) -> dict:
        """
        Authenticate a user.

        Only active and email-verified users
        are allowed to receive authentication tokens.
        """

        user = self.users.get_by_email(
            email
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not user.active:
            raise ValueError(
                "Account inactive."
            )

        # ------------------------------------------------------
        # Email verification requirement
        # ------------------------------------------------------

        if not user.verified:
            raise ValueError(
                "Please verify your email before logging in."
            )

        # ------------------------------------------------------
        # Password verification
        # ------------------------------------------------------

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        # ------------------------------------------------------
        # Login timestamp
        # ------------------------------------------------------

        user.last_login = datetime.now(timezone.utc)

        self.users.update(
            user
        )

        # ------------------------------------------------------
        # Access token
        # ------------------------------------------------------

        access_token = (
            jwt_service.create_access_token(
                subject=str(user.id)
            )
        )

        # ------------------------------------------------------
        # Refresh token
        # ------------------------------------------------------

        refresh_token = (
            jwt_service.create_refresh_token(
                subject=str(user.id)
            )
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # ==========================================================
    # Refresh Token
    # ==========================================================

    def refresh(
        self,
        refresh_token: str,
    ) -> dict:
        """
        Generate a new access token from
        a valid refresh token.
        """

        # ------------------------------------------------------
        # Validate refresh token
        # ------------------------------------------------------

        payload = (
            jwt_service.decode_refresh_token(
                refresh_token
            )
        )

        # ------------------------------------------------------
        # Extract user ID
        # ------------------------------------------------------

        user_id = payload.get(
            "sub"
        )

        if not user_id:
            raise ValueError(
                "Invalid refresh token."
            )

        # ------------------------------------------------------
        # Load user
        # ------------------------------------------------------

        user = self.users.get(
            user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        # ------------------------------------------------------
        # Account status
        # ------------------------------------------------------

        if not user.active:
            raise ValueError(
                "Account inactive."
            )

        # ------------------------------------------------------
        # Email verification requirement
        # ------------------------------------------------------

        if not user.verified:
            raise ValueError(
                "Please verify your email before using the account."
            )

        # ------------------------------------------------------
        # Create new access token
        # ------------------------------------------------------

        access_token = (
            jwt_service.create_access_token(
                subject=str(user.id)
            )
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }