from __future__ import annotations

import logging

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from app.engine.intelligence.intelligence_engine import (
    IntelligenceEngine,
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

    Pipeline

        Read
          ↓
        Analyze
          ↓
        Intelligence
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

        self._intelligence = IntelligenceEngine(
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

        # ----------------------------------
        # Parse document
        # ----------------------------------

        document = DocumentParser.parse(
            input_docx,
        )

        # ----------------------------------
        # Analyze
        # ----------------------------------

        analysis = self._analyzer.analyze(
            document=document,
            job_description=job_description,
        )

        # ----------------------------------
        # Build optimization strategy
        # ----------------------------------

        strategy = self._intelligence.build(
            analysis,
        )

        # ----------------------------------
        # Build optimization plan
        # ----------------------------------

        plan = self._planner.build(
            strategy=strategy,
            document=document,
        )

        # ----------------------------------
        # Optimize
        # ----------------------------------

        request = OptimizationRequest(
            document=document,
            plan=plan,
        )

        result = self._optimizer.optimize(
            request,
        )

        # ----------------------------------
        # Write optimized DOCX
        # ----------------------------------

        self._writer.write(
            result=result,
            source_file=input_docx,
            output_file=output_docx,
        )

        logger.info(
            "Resume optimization completed successfully."
        )

        return result.document