from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class GuestSession(Base):
    """
    Represents a single anonymous browsing session.

    A Guest may create multiple GuestSessions over time.
    A session may later become associated with a registered user
    after authentication.

    Every user action during the session is recorded through
    UsageEvent records.
    """

    __tablename__ = "guest_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    guest_id: Mapped[str] = mapped_column(
        ForeignKey(
            "guests.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    session_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        String(10),
        default="IN",
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    guest: Mapped["Guest"] = relationship(
        "Guest",
        back_populates="sessions",
    )

    user: Mapped["User | None"] = relationship(
        "User",
    )

    usage_events: Mapped[list["UsageEvent"]] = relationship(
        "UsageEvent",
        back_populates="guest_session",
        cascade="all, delete-orphan",
    )

    @property
    def is_authenticated(self) -> bool:
        """Returns True if this guest session has been linked to a user."""
        return self.user_id is not None

    @property
    def is_active(self) -> bool:
        """Returns whether the session is currently active."""
        return self.active

    def __repr__(self) -> str:
        return (
            f"<GuestSession("
            f"id={self.id}, "
            f"guest_id={self.guest_id}, "
            f"active={self.active}"
            f")>"
        )