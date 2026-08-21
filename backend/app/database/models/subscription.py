from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Subscription(Base):
    """
    Represents an active or historical subscription for a user.

    A subscription is created after a successful order/payment and
    determines the user's access to premium ResumeOptimizer features.

    The payment-provider subscription ID is stored separately from
    the local subscription ID so the application can map local billing
    state to Stripe (or another provider) safely.
    """

    __tablename__ = "subscriptions"

    # ==========================================================
    # Identity
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
        index=True,
        nullable=False,
    )

    # ==========================================================
    # Order
    # ==========================================================

    order_id: Mapped[str] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        unique=True,
        index=True,
        nullable=False,
    )

    # ==========================================================
    # Payment Provider
    # ==========================================================

    provider_subscription_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
    )

    # ==========================================================
    # Subscription State
    # ==========================================================

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    auto_renew: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================================================
    # Subscription Period
    # ==========================================================

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="subscriptions",
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="subscription",
    )

    # ==========================================================
    # Helpers
    # ==========================================================

    @property
    def is_active(self) -> bool:
        """
        Return True when the subscription is currently active
        and has not expired.
        """

        return (
            self.status == "active"
            and self.expires_at > datetime.now(timezone.utc)
        )

    # ==========================================================
    # Representation
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<Subscription("
            f"id={self.id}, "
            f"status={self.status}, "
            f"provider_subscription_id="
            f"{self.provider_subscription_id}, "
            f"expires_at={self.expires_at}"
            f")>"
        )