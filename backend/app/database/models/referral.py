from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Referral(Base):

    __tablename__ = "referrals"

    __table_args__ = (
        UniqueConstraint(
            "referrer_guest_id",
            "referred_guest_id",
            name="uq_referral_referrer_referred",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    referrer_guest_id: Mapped[str] = mapped_column(
        ForeignKey(
            "guests.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    referred_guest_id: Mapped[str] = mapped_column(
        ForeignKey(
            "guests.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False,
    )

    reward_granted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    rewarded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )