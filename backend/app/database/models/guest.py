from __future__ import annotations

import uuid
from datetime import datetime, timezone
from secrets import token_urlsafe

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Guest(Base):
    """
    Represents an anonymous visitor before authentication.

    A Guest is identified by a persistent browser identifier and may
    later become associated with a registered user.

    Guest sessions are tracked separately to support multiple visits.
    """

    __tablename__ = "guests"

    # ============================================================
    # Primary Key
    # ============================================================

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ============================================================
    # Anonymous Identity
    # ============================================================

    browser_id: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        index=True,
        nullable=False,
    )

    referral_code: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        nullable=False,
        default=token_urlsafe,
    )

    # ============================================================
    # Locale
    # ============================================================

    country: Mapped[str] = mapped_column(
        String(5),
        default="IN",
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
    )

    # ============================================================
    # Request Information
    # ============================================================

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ============================================================
    # Optional Registered User
    # ============================================================

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ============================================================
    # Timestamps
    # ============================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user: Mapped["User | None"] = relationship(
        "User",
    )

    sessions: Mapped[list["GuestSession"]] = relationship(
        "GuestSession",
        back_populates="guest",
        cascade="all, delete-orphan",
    )

    # ============================================================
    # Properties
    # ============================================================

    @property
    def is_registered(self) -> bool:
        """Return True if this guest has been linked to a user account."""
        return self.user_id is not None

    # ============================================================
    # Debug
    # ============================================================

    def __repr__(self) -> str:
        return (
            f"<Guest("
            f"id={self.id}, "
            f"browser_id={self.browser_id}, "
            f"country={self.country}, "
            f"registered={self.is_registered}"
            f")>"
        )