from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class GeneratedResume(Base):
    """
    AI-optimized resume generated from an OptimizationJob.

    Each OptimizationJob produces exactly one GeneratedResume.
    The original Resume always remains unchanged.
    """

    __tablename__ = "generated_resumes"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    optimization_job_id: Mapped[str] = mapped_column(
        ForeignKey(
            "optimization_jobs.id",
            ondelete="CASCADE",
        ),
        unique=True,
        index=True,
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    optimization_job: Mapped["OptimizationJob"] = relationship(
        "OptimizationJob",
        back_populates="generated_resume",
    )

    downloads: Mapped[list["Download"]] = relationship(
        "Download",
        back_populates="resume_output",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<GeneratedResume("
            f"id={self.id}, "
            f"filename={self.filename}"
            f")>"
        )