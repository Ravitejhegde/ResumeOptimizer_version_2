from __future__ import annotations


from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session


from app.core.security.jwt import (
    jwt_service,
)

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
    token: str = Depends(
        oauth2_scheme,
    ),
    db: Session = Depends(
        get_db,
    ),
) -> User:
    """
    Get authenticated user from JWT token.
    """


    try:

        user_id = jwt_service.get_user_id(
            token,
        )


    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc



    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.active.is_(True),
        )
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive.",
        )


    return user