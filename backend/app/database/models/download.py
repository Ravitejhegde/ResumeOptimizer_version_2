from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Download(Base):
    """
    Records each download of an optimized resume.

    Every download is stored for analytics, usage tracking,
    auditing, and subscription limit enforcement.
    """

    __tablename__ = "downloads"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    resume_output_id: Mapped[str] = mapped_column(
        ForeignKey(
            "generated_resumes.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        default="docx",
        nullable=False,
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    resume_output: Mapped["GeneratedResume"] = relationship(
        "GeneratedResume",
        back_populates="downloads",
    )

    def __repr__(self) -> str:
        return (
            f"<Download("
            f"id={self.id}, "
            f"file_type={self.file_type}, "
            f"downloaded_at={self.downloaded_at}"
            f")>"
        )