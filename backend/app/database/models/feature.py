from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Feature(Base):
    """
    Represents a capability that can be assigned to one or more
    subscription plans.

    Examples:
        - Unlimited Optimizations
        - Resume History
        - PDF Download
        - Priority Queue
        - AI Resume Rewrite
        - Cover Letter Generation

    The actual value of a feature for a specific plan is stored
    in the PlanFeature model.
    """

    __tablename__ = "features"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    value_type: Mapped[str] = mapped_column(
        String(20),
        default="boolean",
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

    plan_features: Mapped[list["PlanFeature"]] = relationship(
        "PlanFeature",
        back_populates="feature",
        cascade="all, delete-orphan",
    )

    @property
    def is_active(self) -> bool:
        """Returns whether this feature is currently enabled."""
        return self.active

    def __repr__(self) -> str:
        return (
            f"<Feature("
            f"id={self.id}, "
            f"code={self.code}, "
            f"name={self.name}, "
            f"value_type={self.value_type}, "
            f"active={self.active}"
            f")>"
        )