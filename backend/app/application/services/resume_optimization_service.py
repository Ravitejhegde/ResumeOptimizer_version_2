from __future__ import annotations

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


class ResumeOptimizationService:
    """
    Public entry point for resume optimization.
    """

    def __init__(self) -> None:

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

        return self._workflow.execute(
            request
        )