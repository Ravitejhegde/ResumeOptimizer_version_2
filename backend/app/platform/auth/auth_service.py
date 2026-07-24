import uuid
from datetime import datetime

from .auth_repository import AuthRepository
from app.platform.users.models import User


class AuthService:
    """
    Handles user registration and authentication.

    This service is the single entry point for:
    - Google Login
    - Email OTP Login
    - Guest → User migration
    """

    @classmethod
    def register(
        cls,
        email: str,
        name: str,
        provider: str,
        guest_id: str | None = None,
    ) -> User:

        existing = AuthRepository.get_by_email(email)

        if existing:
            return existing

        now = datetime.utcnow()

        user = User(

            id=str(uuid.uuid4()),

            email=email.strip().lower(),

            name=name.strip(),

            provider=provider,

            plan="free",

            verified=True,

            created_at=now,

            last_login=now,

            guest_id=guest_id,

        )

        AuthRepository.save(user)

        return user

    @classmethod
    def login(
        cls,
        email: str,
    ) -> User | None:

        user = AuthRepository.get_by_email(email)

        if user:

            user.last_login = datetime.utcnow()

            AuthRepository.save(user)

        return user

    @classmethod
    def get_user(
        cls,
        user_id: str,
    ) -> User | None:

        return AuthRepository.get_by_id(user_id)

    @classmethod
    def merge_guest(
        cls,
        user: User,
        guest_id: str,
    ) -> User:
        """
        Attach a guest identity to
        an existing account.

        Later this will also migrate:
        - Usage
        - Resume history
        - Drafts
        """

        user.guest_id = guest_id

        AuthRepository.save(user)

        return user