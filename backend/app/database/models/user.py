from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    """
    Registered application user.
    """

    __tablename__ = "users"


    # ==========================================================
    # Primary Key
    # ==========================================================

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


    # ==========================================================
    # Authentication
    # ==========================================================

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )


    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    # ==========================================================
    # Profile
    # ==========================================================

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )


    provider: Mapped[str] = mapped_column(
        String(30),
        default="email",
        nullable=False,
    )


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


    # ==========================================================
    # Account Status
    # ==========================================================

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


    # ==========================================================
    # Timestamps
    # ==========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    # ==========================================================
    # Relationships
    # ==========================================================

    workspace: Mapped["Workspace | None"] = relationship(
        "Workspace",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    usage_events: Mapped[list["UsageEvent"]] = relationship(
        "UsageEvent",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    # ==========================================================
    # Debug
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, email={self.email})>"
        )