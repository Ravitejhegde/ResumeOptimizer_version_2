from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.repositories.user_repository import (
    UserRepository,
)


class UserService:
    """
    Business logic for users.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.users = UserRepository(db)

    def get_user(
        self,
        user_id: str,
    ) -> User | None:

        return self.users.get(user_id)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return self.users.get_by_email(email)

    def create_user(
        self,
        user: User,
    ) -> User:

        return self.users.create(user)

    def update_user(
        self,
        user: User,
    ) -> User:

        return self.users.update(user)

    def deactivate_user(
        self,
        user: User,
    ) -> User:

        return self.users.deactivate(user)