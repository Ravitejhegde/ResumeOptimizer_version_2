from __future__ import annotations

import logging

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.models.resume import Resume

from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.services.storage.storage_service import (
    StorageService,
)


logger = logging.getLogger(__name__)


class ResumeService:
    """
    Business service for resume lifecycle.

    Responsibilities:
        - Upload resume
        - Create resume database record
        - Retrieve resumes
        - Delete resumes

    Does not:
        - Parse documents
        - Analyze resumes
        - Optimize resumes
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self.resumes = ResumeRepository(
            db
        )

        self.storage = StorageService()


    # ======================================================
    # Queries
    # ======================================================

    def get_resume(
        self,
        resume_id: str,
    ) -> Resume | None:

        return self.resumes.get(
            resume_id
        )


    def get_workspace_resumes(
        self,
        workspace_id: str,
    ) -> list[Resume]:

        return self.resumes.get_by_workspace(
            workspace_id
        )


    def count_workspace_resumes(
        self,
        workspace_id: str,
    ) -> int:

        return self.resumes.count_by_workspace(
            workspace_id
        )


    # ======================================================
    # Upload
    # ======================================================

    async def upload_resume(
        self,
        workspace_id: str,
        file: UploadFile,
    ) -> Resume:
        """
        Save resume file and create database record.
        """

        try:

            # ----------------------------------
            # Save physical file
            # ----------------------------------

            stored = await self.storage.save_upload(
                file
            )


            # ----------------------------------
            # Create resume record
            # ----------------------------------

            resume = Resume(

                workspace_id=workspace_id,

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


            logger.info(
                "Resume uploaded successfully: %s",
                created.id,
            )


            return created


        except Exception as exc:

            logger.exception(
                "Resume upload failed"
            )

            raise exc



    # ======================================================
    # Delete
    # ======================================================

    def delete_resume(
        self,
        resume: Resume,
    ) -> bool:
        """
        Delete resume file and database record.
        """


        deleted = self.storage.delete(
            resume.file_path
        )


        self.resumes.delete(
            resume
        )


        logger.info(
            "Resume deleted: %s",
            resume.id,
        )


        return deleted