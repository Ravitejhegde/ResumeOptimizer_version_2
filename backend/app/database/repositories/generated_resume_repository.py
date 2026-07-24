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
    Repository for GeneratedResume operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            GeneratedResume,
            db,
        )

    def get_by_job(
        self,
        optimization_job_id: str,
    ) -> GeneratedResume | None:

        return (
            self.db.query(
                GeneratedResume
            )
            .filter(
                GeneratedResume.optimization_job_id
                == optimization_job_id
            )
            .first()
        )

    def exists(
        self,
        optimization_job_id: str,
    ) -> bool:

        return (
            self.db.query(
                GeneratedResume
            )
            .filter(
                GeneratedResume.optimization_job_id
                == optimization_job_id
            )
            .first()
            is not None
        )