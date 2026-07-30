from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Order(Base):
    """
    Represents a purchase made by a user.

    An order records the selected pricing option and payment amount.
    Once payment succeeds, a Subscription is created for the user.

    Workflow:
        User
          ↓
        Order
          ↓
        PaymentTransaction(s)
          ↓
        Subscription
    """

    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    pricing_id: Mapped[str] = mapped_column(
        ForeignKey(
            "pricing.id",
            ondelete="RESTRICT",
        ),
        index=True,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
    )

    pricing: Mapped["Pricing"] = relationship(
        "Pricing",
        back_populates="orders",
    )

    subscription: Mapped["Subscription | None"] = relationship(
        "Subscription",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    payment_transactions: Mapped[list["PaymentTransaction"]] = relationship(
        "PaymentTransaction",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    @property
    def is_paid(self) -> bool:
        """Returns True if the order has been successfully paid."""
        return self.status == "paid"

    def __repr__(self) -> str:
        return (
            f"<Order("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"amount={self.amount} {self.currency}, "
            f"status={self.status}"
            f")>"
        )