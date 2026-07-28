from __future__ import annotations

import logging

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from app.engine.models.document.document import (
    Document,
)
from app.engine.models.optimizer.optimization_request import (
    OptimizationRequest,
)
from app.engine.optimizer.optimizer_engine import (
    OptimizerEngine,
)
from app.engine.planner.planner_engine import (
    PlannerEngine,
)
from app.engine.reader.parser import (
    DocumentParser,
)
from app.engine.writer.writer_engine import (
    WriterEngine,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)

logger = logging.getLogger(__name__)


class ResumeOptimizationEngine:
    """
    ResumeOptimizer V3

    Central orchestration engine.

    Pipeline

        Read
          ↓
        Analyze
          ↓
        Plan
          ↓
        Optimize
          ↓
        Write
    """

    def __init__(
        self,
    ) -> None:

        self._knowledge = KnowledgeManager()
        self._knowledge.initialize()

        self._analyzer = DocumentAnalyzer(
            self._knowledge,
        )

        self._planner = PlannerEngine()

        self._optimizer = OptimizerEngine()

        self._writer = WriterEngine()

    # --------------------------------------------------

    def optimize(
        self,
        input_docx: str,
        output_docx: str,
        selected_skills: list[str],
        job_description: str | None = None,
    ) -> Document:

        document = DocumentParser.parse(
            input_docx,
        )

        analysis = self._analyzer.analyze(
            document=document,
            job_description=job_description,
        )

        plan = self._planner.build(
            document=document,
            analysis=analysis,
            selected_skills=selected_skills,
        )

        request = OptimizationRequest(
            document=document,
            plan=plan,
        )

        result = self._optimizer.optimize(
            request,
        )

        self._writer.write(
            result=result,
            source_file=input_docx,
            output_file=output_docx,
        )

        logger.info(
            "Resume optimization completed successfully."
        )

        return result.document