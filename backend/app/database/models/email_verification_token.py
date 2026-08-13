"""
app.database.models.email_verification_token

Stores single-use email verification tokens.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class EmailVerificationToken(Base):
    """
    Single-use token used to verify ownership of a user's email address.

    The raw token is never stored in the database.
    Only its hash will be stored by the service layer.
    """

    __tablename__ = "email_verification_tokens"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ==========================================================
    # User
    # ==========================================================

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Token
    # ==========================================================

    token_hash: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Expiration
    # ==========================================================

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Usage
    # ==========================================================

    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ==========================================================
    # Timestamps
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ==========================================================
    # Relationship
    # ==========================================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_verification_tokens",
    )

    # ==========================================================
    # Helpers
    # ==========================================================

    @property
    def is_expired(self) -> bool:
        """
        Return True when the token has expired.
        """

        return (
            datetime.now(timezone.utc)
            >= self.expires_at
        )

    @property
    def is_valid(self) -> bool:
        """
        Return True when the token can still be used.
        """

        return (
            not self.used
            and not self.is_expired
        )

    def mark_used(self) -> None:
        """
        Mark the token as consumed.
        """

        self.used = True

        self.used_at = (
            datetime.now(timezone.utc)
        )