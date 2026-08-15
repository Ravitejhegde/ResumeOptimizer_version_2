from __future__ import annotations

import logging

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.models.guest_resume import GuestResume
from app.database.repositories.guest_resume_repository import (
    GuestResumeRepository,
)
from app.services.storage.storage_service import StorageService


logger = logging.getLogger(__name__)


class GuestResumeService:
    """
    Business logic for guest resume lifecycle.

    Responsibilities:
        - Upload guest resume
        - Create guest resume database record
        - Retrieve guest resumes
        - Delete guest resumes

    Does not:
        - Analyze resumes
        - Optimize resumes
        - Manage registered-user resumes
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

        self.resumes = GuestResumeRepository(
            db
        )

        self.storage = StorageService()

    # ==========================================================
    # Queries
    # ==========================================================

    def get_resume(
        self,
        resume_id: str,
    ) -> GuestResume | None:
        """
        Return a guest resume by ID.
        """

        return self.resumes.get_by_id(
            resume_id
        )

    def get_guest_resumes(
        self,
        guest_id: str,
    ) -> list[GuestResume]:
        """
        Return all resumes belonging to a guest.
        """

        return self.resumes.get_by_guest(
            guest_id
        )

    def count_guest_resumes(
        self,
        guest_id: str,
    ) -> int:
        """
        Return the number of resumes belonging to a guest.
        """

        return self.resumes.count_by_guest(
            guest_id
        )

    # ==========================================================
    # Upload
    # ==========================================================

    async def upload_resume(
        self,
        guest_id: str,
        file: UploadFile,
    ) -> GuestResume:
        """
        Save a guest resume file and create its database record.
        """

        try:
            # --------------------------------------------------
            # Save physical file
            # --------------------------------------------------

            stored = await self.storage.save_upload(
                file
            )

            # --------------------------------------------------
            # Create database record
            # --------------------------------------------------

            resume = GuestResume(
                guest_id=guest_id,

                original_filename=(
                    stored.original_filename
                ),

                stored_filename=(
                    stored.stored_filename
                ),

                file_path=str(
                    stored.file_path
                ),

                file_size=(
                    stored.file_size
                ),

                status="uploaded",
            )

            created = self.resumes.create(
                resume
            )

            self.db.commit()
            self.db.refresh(created)

            logger.info(
                "Guest resume uploaded successfully: %s",
                created.id,
            )

            return created

        except Exception:
            self.db.rollback()

            logger.exception(
                "Guest resume upload failed"
            )

            raise

    # ==========================================================
    # Delete
    # ==========================================================

    def delete_resume(
        self,
        resume: GuestResume,
    ) -> bool:
        """
        Delete the physical file and database record.
        """

        deleted = self.storage.delete(
            resume.file_path
        )

        self.resumes.delete(
            resume
        )

        self.db.commit()

        logger.info(
            "Guest resume deleted: %s",
            resume.id,
        )

        return deleted