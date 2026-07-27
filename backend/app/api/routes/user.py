from fastapi import APIRouter
from fastapi import Depends

from app.core.security.dependencies import (
    get_current_user,
)
from app.database.models.user import User
from app.schemas.token import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user,
    ),
):

    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        provider=current_user.provider,
        verified=current_user.verified,
        active=current_user.active,
    )




