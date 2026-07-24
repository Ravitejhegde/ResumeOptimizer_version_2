from app.platform.users.models import User


class AuthRepository:
    """
    Temporary in-memory repository.

    Replace with SQLAlchemy later.
    """

    _users: dict[str, User] = {}

    @classmethod
    def save(
        cls,
        user: User,
    ) -> None:

        cls._users[user.id] = user

    @classmethod
    def get_by_id(
        cls,
        user_id: str,
    ) -> User | None:

        return cls._users.get(user_id)

    @classmethod
    def get_by_email(
        cls,
        email: str,
    ) -> User | None:

        for user in cls._users.values():

            if user.email.lower() == email.lower():
                return user

        return None

    @classmethod
    def exists(
        cls,
        email: str,
    ) -> bool:

        return (
            cls.get_by_email(email)
            is not None
        )