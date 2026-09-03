"""
app.application.workflows.optimization_workflow

Coordinates the complete resume optimization workflow.
"""

from __future__ import annotations

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)

from app.job_description.services.job_description_parser import (
    JobDescriptionParser,
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

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)

from app.knowledge.builder.knowledge_builder import (
    KnowledgeBuilder,
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

from app.optimizer.models.optimization_request import (
    OptimizationRequest as OptimizerRequest,
)


class OptimizationWorkflow:
    """
    Coordinates the complete resume optimization workflow.

    Contains NO business logic.
    """

    def __init__(
        self,
        analyzer: DocumentAnalyzer,
        resume_understanding: ResumeUnderstandingService,
        job_understanding: JobUnderstandingService,
        gap_analysis: GapAnalysisService,
        planner: Planner,
        optimizer: Optimizer,
        writer: Writer,
    ) -> None:

        self._analyzer = analyzer

        self._resume_understanding = (
            resume_understanding
        )

        self._job_understanding = (
            job_understanding
        )

        self._gap_analysis = (
            gap_analysis
        )

        self._knowledge_builder = KnowledgeBuilder(
            KnowledgeManager()
        )

        self._planner = (
            planner
        )

        self._optimizer = (
            optimizer
        )

        self._writer = (
            writer
        )

        self._job_parser = (
            JobDescriptionParser()
        )

    def execute(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResponse:
        """
        Execute the complete optimization workflow.
        """

        # ----------------------------------
        # 1. Analyze Resume
        # ----------------------------------

        document = self._analyzer.analyze(
            request.resume_path
        )

        # ----------------------------------
        # 2. Resume Understanding
        # ----------------------------------

        resume = (
            self._resume_understanding.understand(
                document
            )
        )

        # ----------------------------------
        # 3. Parse Job Description
        # ----------------------------------

        job_description = (
            self._job_parser.parse(
                request.job_description
            )
        )

        # ----------------------------------
        # 4. Job Understanding
        # ----------------------------------

        job = (
            self._job_understanding.understand(
                job_description
            )
        )

        # ----------------------------------
        # 5. Gap Analysis
        # ----------------------------------

        gap = (
            self._gap_analysis.analyze(
                resume=resume,
                job=job,
            )
        )

        # ----------------------------------
        # 6. Knowledge Builder
        # ----------------------------------

        knowledge = (
            self._knowledge_builder.build(
                role_id=request.role_id,
                matched_skills=gap.matched_skills,
                selected_missing_skills=request.selected_skills,
            )
        )

        # ----------------------------------
        # 7. Planning
        # ----------------------------------

        blueprint = (
            self._planner.build(
                document=document,
                resume=resume,
                job=job,
                gap=gap,
                knowledge=knowledge,
            )
        )

        # ----------------------------------
        # 8. Optimizer
        # ----------------------------------

        optimizer_request = (
            OptimizerRequest(
                document=document,
                resume=resume,
                job=job,
                blueprint=blueprint,
            )
        )

        optimization = (
            self._optimizer.optimize(
                optimizer_request
            )
        )

        # ----------------------------------
        # 9. Writer
        # ----------------------------------

        writer_result = (
            self._writer.write(
                source_file=request.resume_path,
                output_file=request.output_path,
                document=document,
                optimization=optimization,
            )
        )

        # ----------------------------------
        # 10. Response
        # ----------------------------------

        return OptimizationResponse(
            success=writer_result.success,
            message=writer_result.message,
            output_path=writer_result.output_path,
        )