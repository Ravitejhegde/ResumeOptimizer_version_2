from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(User, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Returns a user by email.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def email_exists(
        self,
        email: str,
    ) -> bool:
        """
        Returns True if the email already exists.
        """
        return self.get_by_email(email) is not None

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        user: User,
    ) -> User:
        """
        Activates a user account.
        """
        user.active = True
        return self.update(user)

    def deactivate(
        self,
        user: User,
    ) -> User:
        """
        Deactivates a user account.
        """
        user.active = False
        return self.update(user)

    def verify(
        self,
        user: User,
    ) -> User:
        """
        Marks a user as verified.
        """
        user.verified = True
        return self.update(user)

    def unverify(
        self,
        user: User,
    ) -> User:
        """
        Removes the user's verified status.
        """
        user.verified = False
        return self.update(user)