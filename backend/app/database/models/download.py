import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base


class Download(Base):
    """
    Records every download of a generated resume.
    """

    __tablename__ = "downloads"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    resume_output_id: Mapped[str] = mapped_column(
        ForeignKey("generated_resumes.id"),
        nullable=False,
        index=True,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        default="docx",
        nullable=False,
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resume_output: Mapped["GeneratedResume"] = relationship(
        "GeneratedResume",
        back_populates="downloads",
    )




