"""
Email verification token repository.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.email_verification_token import (
    EmailVerificationToken,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


class EmailVerificationTokenRepository(
    BaseRepository[EmailVerificationToken],
):
    """
    Repository for EmailVerificationToken database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            EmailVerificationToken,
            db,
        )

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> EmailVerificationToken | None:
        """
        Returns a verification token by its hash.
        """

        return (
            self.db.query(
                EmailVerificationToken
            )
            .filter(
                EmailVerificationToken.token_hash
                == token_hash,
            )
            .first()
        )

    def get_active_by_user(
        self,
        user_id: str,
    ) -> EmailVerificationToken | None:
        """
        Returns the latest valid verification token
        belonging to a user.
        """

        now = datetime.now(timezone.utc)

        return (
            self.db.query(
                EmailVerificationToken
            )
            .filter(
                EmailVerificationToken.user_id
                == user_id,
                EmailVerificationToken.used.is_(False),
                EmailVerificationToken.expires_at > now,
            )
            .order_by(
                EmailVerificationToken.created_at.desc(),
            )
            .first()
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def mark_used(
        self,
        token: EmailVerificationToken,
    ) -> EmailVerificationToken:
        """
        Marks a verification token as used.
        """

        token.mark_used()

        return self.update(token)

    # ==========================================================
    # Cleanup
    # ==========================================================

    def delete_for_user(
        self,
        user_id: str,
    ) -> int:
        """
        Deletes all verification tokens belonging
        to a user.

        Returns:
            Number of deleted tokens.
        """

        deleted = (
            self.db.query(
                EmailVerificationToken
            )
            .filter(
                EmailVerificationToken.user_id
                == user_id,
            )
            .delete(
                synchronize_session=False,
            )
        )

        self.db.commit()

        return deleted