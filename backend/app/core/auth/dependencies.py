from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth.jwt import decode_access_token
from app.database.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.database.session import get_db

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(
        get_db,
    ),
) -> User:

    payload = decode_access_token(
        credentials.credentials,
    )

    user_id = payload.get(
        "sub",
    )

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
        )

    user = UserRepository(
        db,
    ).get(
        user_id,
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found.",
        )

    return user




