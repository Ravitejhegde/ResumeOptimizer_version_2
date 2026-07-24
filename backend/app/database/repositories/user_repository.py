from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.repositories.base_repository import (
    BaseRepository,
)


class UserRepository(
    BaseRepository[User],
):
    """
    Repository for User operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            User,
            db,
        )

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def exists(
        self,
        email: str,
    ) -> bool:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
            is not None
        )

    def activate(
        self,
        user: User,
    ) -> User:

        user.active = True

        return self.update(user)

    def deactivate(
        self,
        user: User,
    ) -> User:

        user.active = False

        return self.update(user)