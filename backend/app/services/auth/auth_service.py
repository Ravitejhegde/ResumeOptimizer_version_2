from __future__ import annotations

import logging
import uuid
from datetime import datetime

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
        Create new user account.
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


        # Create default workspace

        self.workspace.create_workspace(
            user_id=user.id
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
        Authenticate user.
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


        if not verify_password(
            password,
            user.password_hash,
        ):

            raise ValueError(
                "Invalid email or password."
            )


        user.last_login = datetime.utcnow()


        self.users.update(
            user
        )


        access_token = (
            jwt_service.create_access_token(
                subject=str(user.id)
            )
        )


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
        Generate new access token.
        """


        payload = (
            jwt_service.decode_token(
                refresh_token
            )
        )


        if payload.get("type") != "refresh":

            raise ValueError(
                "Invalid refresh token."
            )


        user_id = payload.get(
            "sub"
        )


        user = self.users.get(
            user_id
        )


        if user is None:

            raise ValueError(
                "User not found."
            )


        access_token = (
            jwt_service.create_access_token(
                subject=str(user.id)
            )
        )


        return {

            "access_token": access_token,

            "token_type": "bearer",

        }