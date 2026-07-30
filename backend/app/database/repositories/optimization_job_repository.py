from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.optimization_job import OptimizationJob
from app.database.repositories.base_repository import BaseRepository


class OptimizationJobRepository(BaseRepository[OptimizationJob]):
    """
    Repository for OptimizationJob database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(OptimizationJob, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_resume(
        self,
        resume_id: str,
    ) -> list[OptimizationJob]:
        """
        Returns all optimization jobs for a resume,
        ordered by newest first.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.resume_id == resume_id,
            )
            .order_by(
                OptimizationJob.created_at.desc(),
            )
            .all()
        )

    def count_by_resume(
        self,
        resume_id: str,
    ) -> int:
        """
        Returns the number of optimization jobs
        for a resume.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.resume_id == resume_id,
            )
            .count()
        )

    def get_completed(
        self,
    ) -> list[OptimizationJob]:
        """
        Returns all completed optimization jobs.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.status == "completed",
            )
            .all()
        )

    def get_failed(
        self,
    ) -> list[OptimizationJob]:
        """
        Returns all failed optimization jobs.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.status == "failed",
            )
            .all()
        )

    def get_running(
        self,
    ) -> list[OptimizationJob]:
        """
        Returns all currently running optimization jobs.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.status == "running",
            )
            .all()
        )

    def has_completed_job(
        self,
        resume_id: str,
    ) -> bool:
        """
        Returns True if the resume has at least one
        completed optimization.
        """
        return (
            self.db.query(OptimizationJob)
            .filter(
                OptimizationJob.resume_id == resume_id,
                OptimizationJob.status == "completed",
            )
            .first()
            is not None
        )