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



# ==========================================================
# JWT Service
# ==========================================================

class JWTService:
    """
    Handles JWT token creation and validation.
    """


    ALGORITHM = ALGORITHM


    # ------------------------------------------------------
    # Access Token
    # ------------------------------------------------------

    def create_access_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
        **claims: Any,
    ) -> str:
        """
        Create JWT access token.
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

            "exp": expire,

            "iat": datetime.now(
                timezone.utc
            ),

            **claims,
        }


        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )



    # ------------------------------------------------------
    # Refresh Token
    # ------------------------------------------------------

    def create_refresh_token(
        self,
        subject: str,
    ) -> str:
        """
        Create JWT refresh token.
        """

        expire = (
            datetime.now(timezone.utc)
            +
            timedelta(
                days=7
            )
        )


        payload: dict[str, Any] = {

            "sub": subject,

            "type": "refresh",

            "exp": expire,

            "iat": datetime.now(
                timezone.utc
            ),
        }


        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )



    # ------------------------------------------------------
    # Decode Token
    # ------------------------------------------------------

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode and validate JWT.
        """

        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                self.ALGORITHM
            ],
        )



    # ------------------------------------------------------
    # Verify Token
    # ------------------------------------------------------

    def verify_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Verify JWT token.
        """

        return self.decode_token(
            token
        )



    # ------------------------------------------------------
    # Get User ID
    # ------------------------------------------------------

    def get_user_id(
        self,
        token: str,
    ) -> str:
        """
        Extract user id from JWT.
        """

        payload = self.decode_token(
            token
        )


        user_id = payload.get(
            "sub"
        )


        if not user_id:
            raise ValueError(
                "Missing user id in token."
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
    """
    Legacy wrapper.
    """

    return jwt_service.create_access_token(
        subject=subject,
        expires_delta=expires_delta,
        **claims,
    )



def create_refresh_token(
    subject: str,
) -> str:
    """
    Legacy wrapper.
    """

    return jwt_service.create_refresh_token(
        subject
    )



def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Legacy wrapper.
    """

    return jwt_service.decode_token(
        token
    )



def get_user_id(
    token: str,
) -> str:
    """
    Legacy wrapper.
    """

    return jwt_service.get_user_id(
        token
    )