from sqlalchemy.orm import Session

from app.database.models.optimization_job import (
    OptimizationJob,
)
from app.database.repositories.optimization_job_repository import (
    OptimizationJobRepository,
)


class OptimizationService:
    """
    Business logic for optimization jobs.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.jobs = OptimizationJobRepository(
            db
        )

    def get_job(
        self,
        job_id: str,
    ) -> OptimizationJob | None:

        return self.jobs.get(job_id)

    def get_resume_jobs(
        self,
        resume_id: str,
    ) -> list[OptimizationJob]:

        return self.jobs.get_by_resume(
            resume_id
        )

    def create_job(
        self,
        job: OptimizationJob,
    ) -> OptimizationJob:

        return self.jobs.create(job)

    def update_job(
        self,
        job: OptimizationJob,
    ) -> OptimizationJob:

        return self.jobs.update(job)

    def get_completed_jobs(
        self,
    ) -> list[OptimizationJob]:

        return self.jobs.get_completed()

    def get_running_jobs(
        self,
    ) -> list[OptimizationJob]:

        return self.jobs.get_running()

    def get_failed_jobs(
        self,
    ) -> list[OptimizationJob]:

        return self.jobs.get_failed()