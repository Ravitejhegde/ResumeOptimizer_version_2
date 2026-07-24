import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class OptimizationJob(Base):
    """
    Represents one AI optimization request.

    Each job:
    - Uses one original resume
    - Uses one job description
    - Produces one generated resume
    """

    __tablename__ = "optimization_jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    resume_id: Mapped[str] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
        index=True,
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
        DateTime,
        default=datetime.utcnow,
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