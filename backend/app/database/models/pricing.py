import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Pricing(Base):
    """
    Country-specific pricing for a subscription plan.
    """

    __tablename__ = "pricing"

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

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
        index=True,
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    monthly_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    yearly_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    payment_provider: Mapped[str] = mapped_column(
        String(50),
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




