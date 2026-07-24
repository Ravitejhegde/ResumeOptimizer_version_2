import uuid
from datetime import datetime

from .models import User
from .user_repository import UserRepository


class UserService:

    @classmethod
    def create(
        cls,
        email: str,
        name: str,
        provider: str,
        guest_id: str | None = None,
    ) -> User:

        existing = UserRepository.get_by_email(
            email
        )

        if existing:
            return existing

        now = datetime.utcnow()

        user = User(

            id=str(uuid.uuid4()),

            email=email.lower(),

            name=name,

            provider=provider,

            plan="free",

            verified=True,

            created_at=now,

            updated_at=now,

            last_login=now,

            guest_id=guest_id,

        )

        UserRepository.save(user)

        return user

    @classmethod
    def get(
        cls,
        user_id: str,
    ) -> User | None:

        return UserRepository.get(
            user_id
        )

    @classmethod
    def get_by_email(
        cls,
        email: str,
    ) -> User | None:

        return UserRepository.get_by_email(
            email
        )

    @classmethod
    def update(
        cls,
        user: User,
    ):

        user.updated_at = datetime.utcnow()

        UserRepository.save(user)

        return user