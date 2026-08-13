from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)

from app.schemas.token import TokenResponse

from app.services.auth.auth_service import AuthService

from app.services.auth.email_verification_service import (
    EmailVerificationService,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new user account.

    A six-digit verification code is sent
    to the user's email address.
    """

    service = AuthService(db)

    try:
        user = service.register(
            email=request.email,
            password=request.password,
            name=request.name,
        )

        return RegisterResponse(
            message=(
                "Account created. "
                "Please verify your email."
            ),
            email=user.email,
            verified=user.verified,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ==========================================================
# Verify Email
# ==========================================================

@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
)
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    """
    Verify a user's email address using
    their email address and six-digit OTP.
    """

    service = EmailVerificationService(db)

    try:
        user = service.verify_email_for_user(
            email=request.email,
            raw_token=request.otp,
        )

        return VerifyEmailResponse(
            message="Email verified successfully.",
            email=user.email,
            verified=user.verified,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ==========================================================
# Normal Login JSON
# ==========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate a verified user.
    """

    service = AuthService(db)

    try:
        result = service.login(
            email=request.email,
            password=request.password,
        )

        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type="bearer",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


# ==========================================================
# Swagger OAuth2 Login
# ==========================================================

@router.post(
    "/token",
    response_model=TokenResponse,
)
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2-compatible login endpoint for Swagger.
    """

    service = AuthService(db)

    try:
        result = service.login(
            email=form_data.username,
            password=form_data.password,
        )

        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type="bearer",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )