from pathlib import Path

from app.core.config import settings


class ResumeRepository:

    @staticmethod
    def get_path(resume_id: str) -> Path | None:

        for file in settings.TEMP_DIR.iterdir():

            if file.stem == resume_id:

                return file

        return None