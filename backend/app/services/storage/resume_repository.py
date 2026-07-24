from pathlib import Path

from sqlalchemy.orm import Session

from app.database.models.resume import Resume


class ResumeRepository:

    @staticmethod
    def get_path(
        db: Session,
        resume_id: str,
    ) -> Path | None:

        resume = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

        if resume is None:
            return None

        return Path(resume.file_path)