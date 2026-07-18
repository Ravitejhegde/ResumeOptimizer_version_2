from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import StorageError
from app.schemas.upload_result import UploadResult


class FileStorage:
    """Handles temporary storage of uploaded resume files."""

    @staticmethod
    async def save(file: UploadFile) -> UploadResult:
        try:
            settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)

            extension = Path(file.filename).suffix.lower()

            resume_id = str(uuid4())
            stored_filename = f"{resume_id}{extension}"

            destination = settings.TEMP_DIR / stored_filename

            content = await file.read()

            destination.write_bytes(content)

            await file.seek(0)

            return UploadResult(
                resume_id=resume_id,
                original_filename=file.filename,
                stored_filename=stored_filename,
                uploaded_at=datetime.now(timezone.utc),
            )

        except Exception as e:
            raise StorageError(
                f"Failed to store uploaded file: {e}"
            ) from e