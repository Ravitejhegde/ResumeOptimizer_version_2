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

    def __init__(self) -> None:

        self._section_executor = SectionExecutor()
        self._paragraph_executor = ParagraphExecutor()
        self._run_executor = RunExecutor()
        self._technology_processor = TechnologyProcessor()
        self._rewrite_processor = RewriteProcessor()
        self._validator = OptimizationValidator()

    # --------------------------------------------------

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:

        document = request.document

        print("\n========== OPTIMIZER ==========")
        print(f"Sections in plan: {len(request.plan.sections)}")

        rewrites = []

        for index, section in enumerate(request.plan.sections, start=1):

            print(f"\nSection {index}: {section}")

            paragraphs = self._section_executor.execute(
                document,
                section,
            )

            print(f"Paragraphs found: {len(paragraphs)}")

            for paragraph in paragraphs:

                print(
                    f"Processing paragraph: "
                    f"{paragraph.id}"
                )

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
                        reason=", ".join(technologies)
                        if technologies
                        else "",
                    )
                )

                print(
                    f"Rewrite created -> "
                    f"id={result.paragraph_id}, "
                    f"success={result.success}"
                )

                rewrites.append(result)

        print("\n========== SUMMARY ==========")
        print(f"Total rewrites created: {len(rewrites)}")
        print("=============================\n")

        result = OptimizationResult(
            document=document,
            rewrites=rewrites,
        )

        validated = self._validator.validate(result)

        print(
            f"Total rewrites after validation: "
            f"{len(validated.rewrites)}"
        )

        return validated