from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile
from starlette import status

from sqlalchemy.orm import Session

from app.database.models.resume import Resume

from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.services.upload.file_validator import (
    FileValidator,
)
from app.services.upload.storage_service import (
    StorageService,
)


class UploadService:
    """
    Commercial upload service.

    Responsible for:

    - validating uploads
    - storing files
    - creating database records

    AI extraction and parsing are handled
    by separate services.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db
        self.repository = ResumeRepository(db)

    async def upload_resume(
        self,
        workspace_id: str,
        file: UploadFile,
    ) -> Resume:

        await FileValidator.validate(file)

        filename, file_path = (
            await StorageService.save_resume(
                file
            )
        )

        file_size = (
            Path(file_path)
            .stat()
            .st_size
        )

        resume = Resume(
            workspace_id=workspace_id,
            original_filename=file.filename,
            stored_filename=filename,
            file_path=file_path,
            file_size=file_size,
            status="uploaded",
        )

        try:

            resume = self.repository.create(
                resume
            )

            return resume

        except Exception:

            StorageService.delete_resume(
                file_path
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to upload resume.",
            )