from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile
from starlette import status


class FileValidator:
    """
    Commercial-grade resume file validator.
    """

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    ALLOWED_EXTENSION = ".docx"

    ALLOWED_CONTENT_TYPES = {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/octet-stream",
    }

    @classmethod
    async def validate(
        cls,
        file: UploadFile,
    ) -> None:

        cls._validate_filename(file)

        cls._validate_content_type(file)

        await cls._validate_size(file)

    @classmethod
    def _validate_filename(
        cls,
        file: UploadFile,
    ) -> None:

        if not file.filename:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is missing.",
            )

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        if extension != cls.ALLOWED_EXTENSION:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only DOCX resumes are supported.",
            )

    @classmethod
    def _validate_content_type(
        cls,
        file: UploadFile,
    ) -> None:

        if (
            file.content_type
            not in cls.ALLOWED_CONTENT_TYPES
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type.",
            )

    @classmethod
    async def _validate_size(
        cls,
        file: UploadFile,
    ) -> None:

        content = await file.read()

        size = len(content)

        await file.seek(0)

        if size > cls.MAX_FILE_SIZE:

            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Resume exceeds the maximum size of 10 MB.",
            )