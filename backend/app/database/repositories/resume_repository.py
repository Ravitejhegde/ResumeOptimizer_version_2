from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.resume import Resume
from app.database.repositories.base_repository import (
    BaseRepository,
)


class ResumeRepository(BaseRepository[Resume]):
    """
    Repository for Resume database operations.

    Responsibilities:
        - Query resume records.
        - Persist resume metadata.
        - Manage workspace resume lookup.

    Does not:
        - Handle files.
        - Parse documents.
        - Optimize resumes.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Resume,
            db,
        )


    # ======================================================
    # Workspace Queries
    # ======================================================

    def get_by_workspace(
        self,
        workspace_id: str,
    ) -> list[Resume]:
        """
        Returns workspace resumes,
        newest first.
        """

        return (
            self.db.query(Resume)
            .filter(
                Resume.workspace_id == workspace_id,
            )
            .order_by(
                Resume.created_at.desc(),
            )
            .all()
        )


    def get_by_stored_filename(
        self,
        stored_filename: str,
    ) -> Resume | None:
        """
        Find resume by physical stored filename.
        """

        return (
            self.db.query(Resume)
            .filter(
                Resume.stored_filename
                ==
                stored_filename,
            )
            .first()
        )


    def count_by_workspace(
        self,
        workspace_id: str,
    ) -> int:
        """
        Count resumes in workspace.
        """

        return (
            self.db.query(Resume)
            .filter(
                Resume.workspace_id
                ==
                workspace_id,
            )
            .count()
        )


    def workspace_has_resumes(
        self,
        workspace_id: str,
    ) -> bool:
        """
        Check whether workspace has resumes.
        """

        return (
            self.count_by_workspace(
                workspace_id
            )
            > 0
        )