from sqlalchemy.orm import Session

from app.database.models.resume import Resume
from app.database.repositories.base_repository import (
    BaseRepository,
)


class ResumeRepository(
    BaseRepository[Resume],
):
    """
    Repository for Resume operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Resume,
            db,
        )

    def get_by_workspace(
        self,
        workspace_id: str,
    ) -> list[Resume]:

        return (
            self.db.query(Resume)
            .filter(
                Resume.workspace_id == workspace_id
            )
            .order_by(
                Resume.created_at.desc()
            )
            .all()
        )

    def count_by_workspace(
        self,
        workspace_id: str,
    ) -> int:

        return (
            self.db.query(Resume)
            .filter(
                Resume.workspace_id == workspace_id
            )
            .count()
        )

    def delete_by_id(
        self,
        resume_id: str,
    ) -> bool:

        resume = self.get(resume_id)

        if resume is None:
            return False

        self.delete(resume)

        return True




