from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.platform.auth.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class RegisterRequest(BaseModel):
    email: str
    name: str
    provider: str = "email"
    guest_id: str | None = None


class LoginRequest(BaseModel):
    email: str


@router.post("/register")
def register(
    request: RegisterRequest,
):

    user = AuthService.register(
        email=request.email,
        name=request.name,
        provider=request.provider,
        guest_id=request.guest_id,
    )

    return {
        "success": True,
        "message": "User registered successfully.",
        "data": user,
    }


@router.post("/login")
def login(
    request: LoginRequest,
):

    user = AuthService.login(
        request.email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {
        "success": True,
        "message": "Login successful.",
        "data": user,
    }