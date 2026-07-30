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
)

from app.schemas.token import TokenResponse

from app.services.auth.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================
# Register
# ==========================

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    try:

        user = service.register(
            email=request.email,
            password=request.password,
            name=request.name,
        )

        tokens = service.login(
            email=user.email,
            password=request.password,
        )


        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type="bearer",
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )



# ==========================
# Normal Login JSON
# ==========================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

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
            status_code=401,
            detail=str(exc),
        )



# ==========================
# Swagger OAuth2 Login
# ==========================

@router.post(
    "/token",
    response_model=TokenResponse,
)
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

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
            status_code=401,
            detail=str(exc),
        )