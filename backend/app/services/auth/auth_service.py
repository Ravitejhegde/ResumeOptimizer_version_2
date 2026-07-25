from sqlalchemy.orm import Session

from app.core.security.jwt import (
    jwt_service,
)

from app.core.security.password import (
    password_hasher,
)

from app.database.models.user import (
    User,
)


class AuthService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------

    def register(

        self,

        email: str,

        password: str,

        full_name: str,

    ) -> User:

        existing = (

            self.db.query(User)

            .filter(

                User.email == email,

            )

            .first()

        )

        if existing:

            raise ValueError(
                "Email already registered."
            )

        user = User(

            email=email,

            full_name=full_name,

            password_hash=password_hasher.hash(
                password
            ),

        )

        self.db.add(
            user
        )

        self.db.commit()

        self.db.refresh(
            user
        )

        return user

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------

    def login(

        self,

        email: str,

        password: str,

    ) -> dict:

        user = (

            self.db.query(User)

            .filter(

                User.email == email,

            )

            .first()

        )

        if user is None:

            raise ValueError(
                "Invalid email or password."
            )

        if not password_hasher.verify(

            password,

            user.password_hash,

        ):

            raise ValueError(
                "Invalid email or password."
            )

        access_token = (

            jwt_service.create_access_token(
                str(user.id)
            )

        )

        refresh_token = (

            jwt_service.create_refresh_token(
                str(user.id)
            )

        )

        return {

            "user": user,

            "access_token": access_token,

            "refresh_token": refresh_token,

            "token_type": "bearer",

        }

    # ---------------------------------------------------------
    # Refresh Token
    # ---------------------------------------------------------

    def refresh(

        self,

        refresh_token: str,

    ) -> dict:

        payload = jwt_service.decode(
            refresh_token
        )

        if payload.get(
            "type"
        ) != "refresh":

            raise ValueError(
                "Invalid refresh token."
            )

        user = (

            self.db.query(User)

            .filter(

                User.id == payload["sub"],

            )

            .first()

        )

        if user is None:

            raise ValueError(
                "User not found."
            )

        access_token = (

            jwt_service.create_access_token(
                str(user.id)
            )

        )

        return {

            "access_token": access_token,

            "token_type": "bearer",

        }