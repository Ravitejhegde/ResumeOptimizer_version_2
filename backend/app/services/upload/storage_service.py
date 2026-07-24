import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    """
    Handles permanent resume storage.
    """

    RESUME_DIRECTORY = "resumes"

    @classmethod
    def get_resume_directory(cls) -> Path:

        directory = (
            Path(settings.STORAGE_PATH)
            / cls.RESUME_DIRECTORY
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory

    @classmethod
    async def save_resume(
        cls,
        file: UploadFile,
    ) -> tuple[str, str]:

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        stored_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        directory = cls.get_resume_directory()

        file_path = (
            directory
            / stored_filename
        )

        with file_path.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return (
            stored_filename,
            str(file_path),
        )

    @classmethod
    def delete_resume(
        cls,
        file_path: str,
    ) -> None:

        path = Path(file_path)

        if path.exists():

            path.unlink()