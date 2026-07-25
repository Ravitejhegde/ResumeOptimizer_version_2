from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.security.jwt import (
    get_user_id,
)

from app.database.models.user import User
from app.database.session import get_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme,
    ),
    db: Session = Depends(
        get_db,
    ),
) -> User:

    try:

        user_id = get_user_id(
            token,
        )

    except Exception:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid access token.",

        )

    user = (

        db.query(User)

        .filter(

            User.id == user_id,

            User.active == True,

        )

        .first()

    )

    if user is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="User not found.",

        )

    return user