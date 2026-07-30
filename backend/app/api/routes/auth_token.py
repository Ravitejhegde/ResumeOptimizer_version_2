from __future__ import annotations


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from sqlalchemy.orm import Session


from app.database.session import get_db

from app.services.auth.auth_service import (
    AuthService,
)

from app.schemas.token import (
    TokenResponse,
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



# ==========================================================
# Swagger OAuth2 Token Login
# ==========================================================

@router.post(
    "/token",
    response_model=TokenResponse,
)
def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2 login endpoint.

    Swagger sends:
        username = email
        password = password
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
            token_type=result["token_type"],
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )