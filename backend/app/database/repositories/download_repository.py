from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.download import Download
from app.database.repositories.base_repository import BaseRepository


class DownloadRepository(BaseRepository[Download]):
    """
    Repository for Download database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Download, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_resume_output(
        self,
        resume_output_id: str,
    ) -> list[Download]:
        """
        Returns all download records for a generated resume,
        ordered by newest first.
        """
        return (
            self.db.query(Download)
            .filter(
                Download.resume_output_id == resume_output_id,
            )
            .order_by(
                Download.downloaded_at.desc(),
            )
            .all()
        )

    def get_latest_download(
        self,
        resume_output_id: str,
    ) -> Download | None:
        """
        Returns the most recent download for a generated resume.
        """
        return (
            self.db.query(Download)
            .filter(
                Download.resume_output_id == resume_output_id,
            )
            .order_by(
                Download.downloaded_at.desc(),
            )
            .first()
        )

    def count_downloads(
        self,
        resume_output_id: str,
    ) -> int:
        """
        Returns the total number of downloads
        for a generated resume.
        """
        return (
            self.db.query(Download)
            .filter(
                Download.resume_output_id == resume_output_id,
            )
            .count()
        )

    def has_downloads(
        self,
        resume_output_id: str,
    ) -> bool:
        """
        Returns True if the generated resume
        has been downloaded at least once.
        """
        return self.count_downloads(resume_output_id) > 0