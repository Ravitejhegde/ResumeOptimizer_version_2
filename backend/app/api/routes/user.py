from fastapi import APIRouter, HTTPException

from app.platform.users.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/{user_id}")
def get_user(
    user_id: str,
):

    user = UserService.get(
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {

        "success": True,

        "data": user,

    }


@router.get("/email/{email}")
def get_user_by_email(
    email: str,
):

    user = UserService.get_by_email(
        email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {

        "success": True,

        "data": user,

    }