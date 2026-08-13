"""
FastAPI dependency for authenticated users.
"""

from __future__ import annotations

import jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.security.jwt import jwt_service
from app.database.models.user import User
from app.database.session import get_db


# ==========================================================
# OAuth2 Scheme
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Authenticate the request and return the current user.

    Flow:

        Authorization header
                ↓
             JWT token
                ↓
        Validate access token
                ↓
           Extract user ID
                ↓
          Load user from DB
                ↓
        Check account active
                ↓
           Return User
    """

    try:
        payload = jwt_service.decode_access_token(
            token,
        )

    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    user = (
        db.query(User)
        .filter(
            User.id == str(user_id),
            User.active.is_(True),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return user