from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UsageEvent(Base):
    """
    Records significant actions performed by either a guest
    or an authenticated user.

    Examples:
        - resume_uploaded
        - optimization_started
        - optimization_completed
        - resume_downloaded
        - subscription_purchased
        - login
        - signup

    These events support analytics, auditing, usage reporting,
    subscription enforcement, and future product insights.
    """

    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    guest_session_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "guest_sessions.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )

    resource_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
    )

    event_metadata: Mapped[str | None] = mapped_column(
        "metadata",
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    guest_session: Mapped["GuestSession | None"] = relationship(
        "GuestSession",
        back_populates="usage_events",
    )

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="usage_events",
    )

    @property
    def is_guest_event(self) -> bool:
        """Returns True if this event belongs to a guest session."""
        return self.guest_session_id is not None

    @property
    def is_user_event(self) -> bool:
        """Returns True if this event belongs to a registered user."""
        return self.user_id is not None

    def __repr__(self) -> str:
        return (
            f"<UsageEvent("
            f"id={self.id}, "
            f"event_type={self.event_type}, "
            f"resource_type={self.resource_type}"
            f")>"
        )