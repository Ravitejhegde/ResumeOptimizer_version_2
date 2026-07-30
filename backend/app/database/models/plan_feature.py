from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class PlanFeature(Base):
    """
    Associates a subscription plan with a feature and its value.

    Examples:
        Free Plan
            monthly_optimizations = "10"

        Pro Plan
            monthly_optimizations = "500"

        Free Plan
            pdf_download = "false"

        Pro Plan
            pdf_download = "true"

    The feature's data type is defined by Feature.value_type,
    while the actual configured value is stored here.
    """

    __tablename__ = "plan_features"

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

    feature_id: Mapped[str] = mapped_column(
        ForeignKey(
            "features.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
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
        back_populates="features",
    )

    feature: Mapped["Feature"] = relationship(
        "Feature",
        back_populates="plan_features",
    )

    @property
    def is_active(self) -> bool:
        """Returns whether this feature assignment is enabled."""
        return self.active

    def __repr__(self) -> str:
        return (
            f"<PlanFeature("
            f"id={self.id}, "
            f"plan_id={self.plan_id}, "
            f"feature_id={self.feature_id}, "
            f"value={self.value}, "
            f"active={self.active}"
            f")>"
        )