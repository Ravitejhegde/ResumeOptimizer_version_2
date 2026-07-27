from sqlalchemy.orm import Session

from app.database.models.optimization_job import (
    OptimizationJob,
)
from app.database.repositories.base_repository import (
    BaseRepository,
)


class OptimizationJobRepository(
    BaseRepository[OptimizationJob],
):
    """
    Repository for OptimizationJob operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            OptimizationJob,
            db,
        )

    def get_by_resume(
        self,
        resume_id: str,
    ) -> list[OptimizationJob]:

        return (
            self.db.query(
                OptimizationJob
            )
            .filter(
                OptimizationJob.resume_id
                == resume_id
            )
            .order_by(
                OptimizationJob.created_at.desc()
            )
            .all()
        )

    def get_completed(
        self,
    ) -> list[OptimizationJob]:

        return (
            self.db.query(
                OptimizationJob
            )
            .filter(
                OptimizationJob.status
                == "completed"
            )
            .all()
        )

    def get_failed(
        self,
    ) -> list[OptimizationJob]:

        return (
            self.db.query(
                OptimizationJob
            )
            .filter(
                OptimizationJob.status
                == "failed"
            )
            .all()
        )

    def get_running(
        self,
    ) -> list[OptimizationJob]:

        return (
            self.db.query(
                OptimizationJob
            )
            .filter(
                OptimizationJob.status
                == "running"
            )
            .all()
        )




