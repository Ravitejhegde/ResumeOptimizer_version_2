from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pricing(Base):
    """
    Pricing configuration for a plan in a specific country/currency.

    Stripe price IDs are stored here when Stripe is the payment provider.
    """

    __tablename__ = "pricing"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plan_id: Mapped[str] = mapped_column(
        ForeignKey(
            "plans.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        index=True,
        nullable=False,
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    monthly_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    yearly_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    payment_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    stripe_monthly_price_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    stripe_yearly_price_id: Mapped[str | None] = mapped_column(
        String(255),
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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    plan: Mapped["Plan"] = relationship(
        "Plan",
        back_populates="pricing",
    )

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="pricing",
        cascade="all, delete-orphan",
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        secondary="orders",
        viewonly=True,
    )

    @property
    def is_active(self) -> bool:
        return self.active

    def __repr__(self) -> str:
        return (
            f"<Pricing("
            f"id={self.id}, "
            f"country={self.country_code}, "
            f"currency={self.currency_code}, "
            f"monthly={self.monthly_price}, "
            f"active={self.active}"
            f")>"
        )