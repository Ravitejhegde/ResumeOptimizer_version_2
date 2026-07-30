from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Plan(Base):
    """
    Represents a subscription plan.

    A plan defines the available features offered to users.
    Actual pricing is stored separately in the Pricing model,
    allowing different currencies, regions, and billing cycles
    without duplicating plans.
    """

    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    features: Mapped[list["PlanFeature"]] = relationship(
        "PlanFeature",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    pricing: Mapped[list["Pricing"]] = relationship(
        "Pricing",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    @property
    def is_active(self) -> bool:
        """Returns whether this plan is currently available."""
        return self.active

    def __repr__(self) -> str:
        return (
            f"<Plan("
            f"id={self.id}, "
            f"code={self.code}, "
            f"name={self.name}, "
            f"active={self.active}"
            f")>"
        )