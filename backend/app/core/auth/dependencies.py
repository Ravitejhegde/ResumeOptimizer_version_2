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

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.core.security.jwt import jwt_service
from app.database.models.user import User
from app.database.repositories.user_repository import (
    UserRepository,
)
from app.database.session import get_db


# ==========================================================
# HTTP Bearer Security
# ==========================================================

security = HTTPBearer()


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(
        get_db
    ),
) -> User:
    """
    Validate the access token and return the
    authenticated database user.

    Authentication flow:

        HTTP Bearer token
                ↓
        JWT validation
                ↓
        Extract user ID
                ↓
        Load user from database
                ↓
        Return User
    """

    token = credentials.credentials

    # ------------------------------------------------------
    # Validate access token
    # ------------------------------------------------------

    try:
        payload = jwt_service.decode_access_token(
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

    # ------------------------------------------------------
    # Extract user ID
    # ------------------------------------------------------

    user_id = payload.get(
        "sub"
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    # ------------------------------------------------------
    # Load user
    # ------------------------------------------------------

    user = UserRepository(
        db
    ).get(
        str(user_id)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user


# ==========================================================
# Current Active User
# ==========================================================

def get_current_active_user(
    current_user: User = Depends(
        get_current_user
    ),
) -> User:
    """
    Return the authenticated active user.

    This dependency provides the authorization
    boundary for future checks such as:

        - Account status
        - Workspace access
        - Subscription access
        - Permissions
    """

    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive.",
        )

    return current_user