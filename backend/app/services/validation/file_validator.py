from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import FileValidationError


class FileValidator:
    """Validates uploaded resume files."""

    @staticmethod
    async def validate(file: UploadFile) -> None:
        if file.filename is None or file.filename.strip() == "":
            raise FileValidationError("Filename is missing.")

        extension = Path(file.filename).suffix.lower()

        if extension not in settings.ALLOWED_EXTENSIONS:
            raise FileValidationError(
                "Only Microsoft Word (.docx) files are supported."
            )

        content = await file.read()

        if len(content) == 0:
            raise FileValidationError(
                "Uploaded file is empty."
            )

        if len(content) > settings.MAX_FILE_SIZE:
            raise FileValidationError(
                f"Maximum allowed file size is {settings.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

        # Reset file pointer for the next service
        await file.seek(0)