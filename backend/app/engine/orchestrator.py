from __future__ import annotations

import logging

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.document import (
    Document,
)
from app.engine.optimizer.optimization_coordinator import (
    OptimizationCoordinator,
)
from app.engine.planner.plan import (
    PlanBuilder,
)
from app.engine.reader.parser import (
    DocumentParser,
)
from app.engine.recovery.recovery_manager import (
    RecoveryManager,
)
from app.engine.validator.validation_coordinator import (
    ValidationCoordinator,
)
from app.engine.writer.docx_writer import (
    DocxWriter,
)

logger = logging.getLogger(__name__)


class ResumeOptimizationEngine:
    """
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
    Validate
        ↓
    Write
    """

    def __init__(self) -> None:

        self._knowledge = KnowledgeBase()
        self._knowledge.initialize()

        self._analyzer = DocumentAnalyzer(
            self._knowledge
        )

        self._planner = PlanBuilder(
            self._knowledge
        )

        self._optimizer = (
            OptimizationCoordinator()
        )

        self._validator = (
            ValidationCoordinator()
        )

        self._recovery = (
            RecoveryManager()
        )

    def optimize(
        self,
        input_docx: str,
        output_docx: str,
        selected_skills: list[str],
    ) -> Document:

        document = DocumentParser.parse(
            input_docx
        )

        backup = self._recovery.backup(
            document
        )

        try:

            analysis = self._analyzer.analyze(
                document
            )

            plan = self._planner.build(
                document=document,
                analysis=analysis,
                selected_skills=selected_skills,
            )

            optimized = self._optimizer.optimize(
                document=document,
                plan=plan,
            )

            validation = (
    self._validator.validate(
        original=document,
        optimized=optimized,
        plan=plan,
    )
)

            if not validation.valid:

                logger.warning(
                    "Optimization validation failed: %s",
                    validation.message,
                )

                return self._recovery.rollback(
                    backup
                )

            DocxWriter.write(
                document=optimized,
                source_file=input_docx,
                output_file=output_docx,
            )

            return optimized

        except Exception:

            logger.exception(
                "Resume optimization failed."
            )

            return self._recovery.rollback(
                backup
            )