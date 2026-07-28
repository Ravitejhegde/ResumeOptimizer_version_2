from __future__ import annotations

from app.engine.models.optimizer.optimization_request import (
    OptimizationRequest,
)
from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)
from app.engine.optimizer.executors.paragraph_executor import (
    ParagraphExecutor,
)
from app.engine.optimizer.executors.run_executor import (
    RunExecutor,
)
from app.engine.optimizer.executors.section_executor import (
    SectionExecutor,
)
from app.engine.optimizer.processors.rewrite_processor import (
    RewriteProcessor,
)
from app.engine.optimizer.processors.technology_processor import (
    TechnologyProcessor,
)
from app.engine.optimizer.validators.optimization_validator import (
    OptimizationValidator,
)


class OptimizerEngine:
    """
    Executes an OptimizationPlan.

    Planner
        ↓
    Optimizer
        ↓
    Writer
    """

    def __init__(
        self,
    ) -> None:

        self._section_executor = (
            SectionExecutor()
        )

        self._paragraph_executor = (
            ParagraphExecutor()
        )

        self._run_executor = (
            RunExecutor()
        )

        self._technology_processor = (
            TechnologyProcessor()
        )

        self._rewrite_processor = (
            RewriteProcessor()
        )

        self._validator = (
            OptimizationValidator()
        )

    # --------------------------------------------------

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:

        document = request.document

        rewrites = []

        for section in request.plan.sections:

            paragraphs = (
                self._section_executor.execute(
                    document,
                    section,
                )
            )

            for paragraph in paragraphs:

                paragraph, applicable = (
                    self._paragraph_executor.execute(
                        paragraph,
                        request.plan.rewrites,
                    )
                )

                runs, applicable = (
                    self._run_executor.execute(
                        paragraph.runs,
                        applicable,
                    )
                )

                _, technologies = (
                    self._technology_processor.process(
                        paragraph,
                        applicable,
                    )
                )

                result = (
                    self._rewrite_processor.process(
                        paragraph=paragraph,
                        optimized_text=paragraph.text,
                        reason=(
                            ", ".join(
                                technologies,
                            )
                            if technologies
                            else ""
                        ),
                    )
                )

                rewrites.append(
                    result,
                )

        result = OptimizationResult(

            document=document,

            rewrites=rewrites,

        )

        return self._validator.validate(
            result,
        )
