from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class PaymentTransaction(Base):
    """
    Represents a single payment attempt for an order.

    An order may have multiple payment attempts until one
    completes successfully.

    Examples:
        Attempt #1 -> Failed
        Attempt #2 -> Failed
        Attempt #3 -> Paid
    """

    __tablename__ = "payment_transactions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    order_id: Mapped[str] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
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

    failure_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
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

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment_transactions",
    )

    @property
    def is_successful(self) -> bool:
        """Returns True if the payment was successful."""
        return self.status == "paid"

    @property
    def is_failed(self) -> bool:
        """Returns True if the payment failed."""
        return self.status == "failed"


    @property
    def is_pending(self) -> bool:
        """Returns True if the payment is awaiting completion."""
        return self.status == "pending"

    def __repr__(self) -> str:
        return (
            f"<PaymentTransaction("
            f"id={self.id}, "
            f"provider={self.provider}, "
            f"amount={self.amount} {self.currency}, "
            f"status={self.status}"
            f")>"
        )