from sqlalchemy.orm import Session

from app.database.models.generated_resume import (
    GeneratedResume,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


class GeneratedResumeRepository(
    BaseRepository[GeneratedResume],
):
    """
    Repository for generated resumes.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            GeneratedResume,
            db,
        )