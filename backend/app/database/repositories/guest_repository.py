from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.repositories.base_repository import BaseRepository


class GuestRepository(BaseRepository[Guest]):
    """
    Repository for Guest database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Guest, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_guest_token(
        self,
        guest_token: str,
    ) -> Guest | None:
        """
        Returns a guest by its guest token.
        """
        return (
            self.db.query(Guest)
            .filter(
                Guest.guest_token == guest_token,
            )
            .first()
        )

    def get_by_user(
        self,
        user_id: str,
    ) -> Guest | None:
        """
        Returns the guest profile associated with a user,
        if one exists.
        """
        return (
            self.db.query(Guest)
            .filter(
                Guest.user_id == user_id,
            )
            .first()
        )

    def guest_token_exists(
        self,
        guest_token: str,
    ) -> bool:
        """
        Returns True if the guest token already exists.
        """
        return self.get_by_guest_token(
            guest_token,
        ) is not None

    def user_has_guest(
        self,
        user_id: str,
    ) -> bool:
        """
        Returns True if the user has an associated guest record.
        """
        return self.get_by_user(
            user_id,
        ) is not None

    # ==========================================================
    # State Management
    # ==========================================================

    def link_to_user(
        self,
        guest: Guest,
        user_id: str,
    ) -> Guest:
        """
        Links a guest record to a registered user.
        """
        guest.user_id = user_id
        return self.update(guest)

    def unlink_user(
        self,
        guest: Guest,
    ) -> Guest:
        """
        Removes the user association from a guest.
        """
        guest.user_id = None
        return self.update(guest)