from sqlalchemy.orm import Session

from app.database.models.resume import Resume
from app.database.repositories.resume_repository import (
    ResumeRepository,
)


class ResumeService:
    """
    Business logic for resumes.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.resumes = ResumeRepository(db)

    def get_resume(
        self,
        resume_id: str,
    ) -> Resume | None:

        return self.resumes.get(resume_id)

    def get_workspace_resumes(
        self,
        workspace_id: str,
    ) -> list[Resume]:

        return self.resumes.get_by_workspace(
            workspace_id
        )

    def create_resume(
        self,
        resume: Resume,
    ) -> Resume:

        return self.resumes.create(resume)

    def update_resume(
        self,
        resume: Resume,
    ) -> Resume:

        return self.resumes.update(resume)

    def delete_resume(
        self,
        resume_id: str,
    ) -> bool:

        return self.resumes.delete_by_id(
            resume_id
        )

    def count_resumes(
        self,
        workspace_id: str,
    ) -> int:

        return self.resumes.count_by_workspace(
            workspace_id
        )