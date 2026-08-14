"""
FastAPI authentication dependencies.

Provides reusable dependencies for:
- JWT access-token validation
- authenticated user lookup
- active-user validation
"""

from __future__ import annotations

import jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.core.security.jwt import jwt_service
from app.database.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.database.session import get_db


# ============================================================
# Authentication Scheme
# ============================================================

bearer_scheme = HTTPBearer(
    auto_error=True,
)
# Backward-compatible public name.
oauth2_scheme = bearer_scheme


# ============================================================
# Current User
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme,
    ),
    db: Session = Depends(
        get_db,
    ),
) -> User:
    """
    Authenticate the current request and return the
    corresponding database User.

    Authentication flow:

        Bearer token
            ↓
        Decode access token
            ↓
        Extract user ID
            ↓
        Find User in database
            ↓
        Return User

    Raises:
        HTTPException 401:
            Invalid or expired token.

        HTTPException 401:
            Token does not contain a user ID.

        HTTPException 401:
            User does not exist.
    """

    token = credentials.credentials

    # --------------------------------------------------------
    # Decode and validate access token
    # --------------------------------------------------------

    try:
        payload = jwt_service.decode_access_token(
        token,
    )

    except (
    jwt.InvalidTokenError,
    ValueError,
) as exc:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    ) from exc

    # --------------------------------------------------------
    # Extract user ID
    # --------------------------------------------------------

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # --------------------------------------------------------
    # Load user
    # --------------------------------------------------------

    user = UserRepository(db).get(
    str(user_id),
)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return user


# ============================================================
# Active User
# ============================================================

def get_current_active_user(
    current_user: User = Depends(
        get_current_user,
    ),
) -> User:
    """
    Return the authenticated active user.

    Raises:
        HTTPException 403:
            Account is inactive.
    """

    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive.",
        )

    return current_user