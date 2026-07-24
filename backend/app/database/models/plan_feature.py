import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class PlanFeature(Base):
    """
    Connects a subscription plan with a feature.

    Example:

    Plan: Free
    Feature: monthly_optimizations
    Value: 3

    Plan: Pro
    Feature: pdf_download
    Value: true
    """

    __tablename__ = "plan_features"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("plans.id"),
        nullable=False,
        index=True,
    )

    feature_id: Mapped[str] = mapped_column(
        ForeignKey("features.id"),
        nullable=False,
        index=True,
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
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
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