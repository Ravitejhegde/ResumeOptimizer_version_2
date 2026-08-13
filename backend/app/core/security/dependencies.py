"""
FastAPI authentication dependencies.
"""

from __future__ import annotations

import jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from app.core.security.jwt import jwt_service


# ==========================================================
# OAuth2 Scheme
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """
    Validate the JWT access token.

    Returns:
        JWT payload.
    """

    try:
        return jwt_service.decode_access_token(
            token
        )

    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc


# ==========================================================
# Active User
# ==========================================================

def get_current_active_user(
    current_user: dict = Depends(
        get_current_user
    ),
) -> dict:
    """
    Return the authenticated user payload.

    Future responsibilities:
        - Verify user exists
        - Verify account is active
        - Verify subscription access
        - Verify workspace permissions
    """

    return current_user