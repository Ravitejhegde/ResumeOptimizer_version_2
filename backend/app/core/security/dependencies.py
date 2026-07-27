from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.security.jwt import (
    get_user_id,
)

from app.database.models.user import User

from app.database.repositories.user_repository import (
    UserRepository,
)

from app.database.session import (
    get_db,
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(
        get_db,
    ),
) -> User:
    """
    Returns the authenticated user.
    """

    try:

        user_id = get_user_id(
            credentials.credentials,
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token.",
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




