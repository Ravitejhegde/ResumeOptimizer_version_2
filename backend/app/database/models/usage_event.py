import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class UsageEvent(Base):
    """
    Records every significant action performed
    by a guest or registered user.
    """

    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    guest_session_id: Mapped[str | None] = mapped_column(
        ForeignKey("guest_sessions.id"),
        nullable=True,
        index=True,
    )

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
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
        DateTime,
        default=datetime.utcnow,
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




