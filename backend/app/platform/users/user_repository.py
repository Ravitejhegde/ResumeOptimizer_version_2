from .models import User


class UserRepository:
    """
    Temporary repository.

    Replace with SQLAlchemy later.
    """

    _users: dict[str, User] = {}

    @classmethod
    def save(
        cls,
        user: User,
    ):

        cls._users[user.id] = user

    @classmethod
    def get(
        cls,
        user_id: str,
    ) -> User | None:

        return cls._users.get(user_id)

    @classmethod
    def get_by_email(
        cls,
        email: str,
    ) -> User | None:

        email = email.lower()

        for user in cls._users.values():

            if user.email.lower() == email:

                return user

        return None

    @classmethod
    def all(
        cls,
    ) -> list[User]:

        return list(
            cls._users.values()
        )