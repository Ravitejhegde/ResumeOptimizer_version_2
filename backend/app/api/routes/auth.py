from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.auth.jwt import create_access_token
from app.core.auth.password import hash_password
from app.core.auth.password import verify_password

from app.database.models.user import User
from app.database.models.workspace import Workspace

from app.database.session import get_db

from app.database.repositories.user_repository import (
    UserRepository,
)
from app.database.repositories.workspace_repository import (
    WorkspaceRepository,
)

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)
from app.schemas.token import (
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    users = UserRepository(db)

    if users.exists(request.email):

        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

    user = User(
        name=request.name,
        email=request.email,
        password=hash_password(
            request.password
        ),
        provider="email",
    )

    user = users.create(user)

    workspace = Workspace(
        user_id=user.id,
        name=f"{user.name}'s Workspace",
    )

    WorkspaceRepository(
        db
    ).create(workspace)

    token = create_access_token(
        user.id
    )

    return TokenResponse(
        access_token=token,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    users = UserRepository(db)

    user = users.get_by_email(
        request.email
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    if not verify_password(
        request.password,
        user.password,
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        user.id
    )

    return TokenResponse(
        access_token=token,
    )