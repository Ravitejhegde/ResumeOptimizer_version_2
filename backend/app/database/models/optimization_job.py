from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OptimizationJob(Base):
    """
    Represents a single resume optimization request.

    Workflow:
        Resume
            ↓
        OptimizationJob
            ↓
        GeneratedResume

    Stores optimization metadata, ATS improvements,
    AI provider information, and processing statistics.
    """

    __tablename__ = "optimization_jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    resume_id: Mapped[str] = mapped_column(
        ForeignKey(
            "resumes.id",
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

    detected_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ats_before: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    ats_after: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    selected_skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    matched_skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    missing_skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    ai_provider: Mapped[str] = mapped_column(
        String(100),
        default="OpenRouter",
        nullable=False,
    )

    ai_model: Mapped[str] = mapped_column(
        String(100),
        default="openai/gpt-4.1-mini",
        nullable=False,
    )

    processing_time: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
        back_populates="optimization_jobs",
    )

    generated_resume: Mapped["GeneratedResume | None"] = relationship(
        "GeneratedResume",
        back_populates="optimization_job",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<OptimizationJob("
            f"id={self.id}, "
            f"status={self.status}, "
            f"ats={self.ats_before}->{self.ats_after}"
            f")>"
        )