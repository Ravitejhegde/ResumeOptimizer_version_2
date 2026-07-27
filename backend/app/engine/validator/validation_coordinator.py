from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document import Document
from app.engine.planner.plan import (
    OptimizationPlan,
)
from app.engine.validator.content_validator import (
    ContentValidator,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Overall validation result.
    """

    valid: bool

    message: str | None = None


class ValidationCoordinator:
    """
    Coordinates validation using the optimization plan.

    Only paragraphs selected for rewriting
    are validated.
    """

    def validate(
        self,
        original: Document,
        optimized: Document,
        plan: OptimizationPlan,
    ) -> ValidationResult:

        original_lookup = {
            paragraph.id: paragraph
            for paragraph in original.paragraphs
        }

        optimized_lookup = {
            paragraph.id: paragraph
            for paragraph in optimized.paragraphs
        }

        for paragraph_id in plan.rewrite_paragraph_ids:

            original_paragraph = original_lookup.get(
                paragraph_id
            )

            optimized_paragraph = optimized_lookup.get(
                paragraph_id
            )

            if (
                original_paragraph is None
                or optimized_paragraph is None
            ):
                continue

            constraints = plan.layout_constraints.get(
                paragraph_id
            )

            result = ContentValidator.validate(
                paragraph=original_paragraph,
                optimized_text=optimized_paragraph.text,
                constraints=constraints,
            )

            if not result.valid:

                return ValidationResult(
                    valid=False,
                    message=result.message,
                )

        return ValidationResult(
            valid=True,
        )




