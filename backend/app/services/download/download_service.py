from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.models.download import Download
from app.database.models.generated_resume import GeneratedResume

from app.database.repositories.download_repository import (
    DownloadRepository,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


logger = logging.getLogger(__name__)


class DownloadService:
    """
    Business logic for generated resume downloads.

    Responsibilities:
    - Validate generated resume
    - Check file availability
    - Create download records
    - Provide download metadata
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._downloads = DownloadRepository(
            db
        )

        self._generated_resumes = BaseRepository(
            GeneratedResume,
            db,
        )

    # ==================================================
    # Download
    # ==================================================

    def create_download(
        self,
        resume_output_id: str,
        file_type: str = "docx",
    ) -> Download:
        """
        Creates a download record.

        Raises:
            FileNotFoundError
            ValueError
        """

        generated_resume = (
            self._generated_resumes.get(
                resume_output_id
            )
        )

        if generated_resume is None:
            raise FileNotFoundError(
                "Generated resume not found."
            )

        file_path = Path(
            generated_resume.file_path
        )

        if not file_path.exists():
            raise FileNotFoundError(
                "Resume file does not exist."
            )

        download = Download(
            resume_output_id=resume_output_id,
            file_type=file_type,
        )

        result = self._downloads.create(
            download
        )

        logger.info(
            "Download created: %s",
            result.id,
        )

        return result

    # ==================================================
    # Queries
    # ==================================================

    def get_download_history(
        self,
        resume_output_id: str,
    ) -> list[Download]:
        """
        Returns download history
        for a generated resume.
        """

        return (
            self._downloads.get_by_resume_output(
                resume_output_id
            )
        )

    def get_download_count(
        self,
        resume_output_id: str,
    ) -> int:
        """
        Returns total downloads.
        """

        return (
            self._downloads.count_downloads(
                resume_output_id
            )
        )

    # ==================================================
    # File Information
    # ==================================================

    def get_file_path(
        self,
        resume_output_id: str,
    ) -> str:
        """
        Returns generated resume file path.
        """

        generated_resume = (
            self._generated_resumes.get(
                resume_output_id
            )
        )

        if generated_resume is None:
            raise FileNotFoundError(
                "Generated resume not found."
            )

        path = Path(
            generated_resume.file_path
        )

        if not path.exists():
            raise FileNotFoundError(
                "File not available."
            )

        return str(path)