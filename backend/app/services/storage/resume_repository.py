from __future__ import annotations

from app.database.models.resume import Resume
from sqlalchemy.orm import Session


class ResumeRepository:
    """
    Database access layer for resume records.

    Responsibilities:
        - Fetch resume metadata.
        - Query resume ownership.
        - Persist resume related data.

    Does not:
        - Handle files.
        - Create paths.
        - Delete storage objects.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db


    def get_by_id(
        self,
        resume_id: str,
    ) -> Resume | None:

        return (
            self.db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )


    def get_file_path(
        self,
        resume_id: str,
    ) -> str | None:
        """
        Returns stored file path metadata.
        """

        resume = self.get_by_id(
            resume_id
        )

        if resume is None:

            return None


        return resume.file_path


    def exists(
        self,
        resume_id: str,
    ) -> bool:

        return (
            self.get_by_id(
                resume_id
            )
            is not None
        )