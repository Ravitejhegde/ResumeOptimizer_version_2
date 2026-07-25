import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Feature(Base):
    """
    A capability that can be enabled
    for one or more subscription plans.

    Examples:
    - Unlimited Optimizations
    - Resume History
    - PDF Download
    - Priority Queue
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
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None]

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

    plan_features: Mapped[list["PlanFeature"]] = relationship(
        "PlanFeature",
        back_populates="feature",
        cascade="all, delete-orphan",
    )