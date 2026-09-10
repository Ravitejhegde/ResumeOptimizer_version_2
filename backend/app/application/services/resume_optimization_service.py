from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)

from app.understanding.services.resume_understanding_service import (
    ResumeUnderstandingService,
)

from app.job_understanding.services.job_understanding_service import (
    JobUnderstandingService,
)

from app.gap_analysis.services.gap_analysis_service import (
    GapAnalysisService,
)

from app.planner.services.planner import (
    Planner,
)

from app.optimizer.services.optimizer import (
    Optimizer,
)

from app.writer.services.writer import (
    Writer,
)

from app.application.models.optimization_request import (
    OptimizationRequest,
)

from app.application.models.optimization_response import (
    OptimizationResponse,
)

from app.application.workflows.optimization_workflow import (
    OptimizationWorkflow,
)

from app.database.models.optimization_job import (
    OptimizationJob,
)

from app.database.models.generated_resume import (
    GeneratedResume,
)

from app.database.repositories.optimization_job_repository import (
    OptimizationJobRepository,
)


class ResumeOptimizationService:
    """
    Public entry point for resume optimization.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._db = db

        self._optimization_jobs = (
            OptimizationJobRepository(db)
        )

        self._workflow = OptimizationWorkflow(

            analyzer=DocumentAnalyzer(),

            resume_understanding=ResumeUnderstandingService(),

            job_understanding=JobUnderstandingService(),

            gap_analysis=GapAnalysisService(),

            planner=Planner(),

            optimizer=Optimizer(),

            writer=Writer(),

        )

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResponse:

        response = self._workflow.execute(
            request
        )

        if not response.success:
            return response

        output_path = Path(
            response.output_path
        )

        if not output_path.exists():
            return OptimizationResponse(
                success=False,
                message=(
                    "Optimization completed, "
                    "but the generated resume "
                    "file could not be found."
                ),
                output_path="",
            )

        job = OptimizationJob(
            resume_id=request.resume_id,
            status="completed",
            selected_skills=",".join(
                request.selected_skills
            ),
            job_description=request.job_description,
        )

        self._optimization_jobs.create_flush(
            job
        )

        generated_resume = GeneratedResume(
            optimization_job_id=job.id,
            filename=output_path.name,
            file_path=str(output_path),
            file_size=output_path.stat().st_size,
        )

        self._db.add(
            generated_resume
        )

        self._db.commit()

        self._db.refresh(
            generated_resume
        )

        return OptimizationResponse(
            success=True,
            message=response.message,
            output_path=response.output_path,
            generated_resume_id=generated_resume.id,
        )