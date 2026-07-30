"""
JWT token utilities.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import settings


# ==========================================================
# Constants
# ==========================================================

ALGORITHM = "HS256"



class JWTService:
    """
    Handles JWT token creation and validation.

    Responsibilities:
        - Create access tokens
        - Create refresh tokens
        - Decode tokens
        - Extract claims

    Does not:
        - Manage users
        - Access database
    """

    ALGORITHM = ALGORITHM



    # ======================================================
    # Access Token
    # ======================================================

    def create_access_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
        **claims: Any,
    ) -> str:
        """
        Create short-lived access token.
        """


        expire = (
            datetime.now(timezone.utc)
            +
            (
                expires_delta
                or timedelta(
                    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
            )
        )


        payload: dict[str, Any] = {

            "sub": subject,

            "type": "access",

            "iat": datetime.now(
                timezone.utc
            ),

            "exp": expire,

            **claims,
        }


        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )



    # ======================================================
    # Refresh Token
    # ======================================================

    def create_refresh_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create long-lived refresh token.
        """


        expire = (
            datetime.now(timezone.utc)
            +
            (
                expires_delta
                or timedelta(
                    days=30
                )
            )
        )


        payload: dict[str, Any] = {

            "sub": subject,

            "type": "refresh",

            "iat": datetime.now(
                timezone.utc
            ),

            "exp": expire,

        }


        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )



    # ======================================================
    # Decode
    # ======================================================

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode and verify JWT signature.
        """


        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                self.ALGORITHM
            ],
        )



    # ======================================================
    # Access Token Validation
    # ======================================================

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode only access tokens.
        """


        payload = self.decode_token(
            token
        )


        if payload.get("type") != "access":

            raise ValueError(
                "Invalid access token."
            )


        return payload



    # ======================================================
    # Refresh Token Validation
    # ======================================================

    def decode_refresh_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode only refresh tokens.
        """


        payload = self.decode_token(
            token
        )


        if payload.get("type") != "refresh":

            raise ValueError(
                "Invalid refresh token."
            )


        return payload



    # ======================================================
    # Extract User ID
    # ======================================================

    def get_user_id(
        self,
        token: str,
    ) -> str:
        """
        Extract user id from token.
        """


        payload = self.decode_token(
            token
        )


        user_id = payload.get(
            "sub"
        )


        if not user_id:

            raise ValueError(
                "Token does not contain user id."
            )


        return str(user_id)



# ==========================================================
# Singleton
# ==========================================================

jwt_service = JWTService()



# ==========================================================
# Backward Compatible Functions
# ==========================================================


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    **claims: Any,
) -> str:

    return jwt_service.create_access_token(
        subject,
        expires_delta,
        **claims,
    )



def create_refresh_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:

    return jwt_service.create_refresh_token(
        subject,
        expires_delta,
    )



def decode_token(
    token: str,
) -> dict[str, Any]:

    return jwt_service.decode_token(
        token
    )



def get_user_id(
    token: str,
) -> str:

    return jwt_service.get_user_id(
        token
    )