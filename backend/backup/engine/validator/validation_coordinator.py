from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document.document import (
    Document,
)

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)

from app.engine.validator.content_validator import (
    ContentValidator,
)

from app.engine.validator.style_validator import (
    StyleValidator,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Overall document validation result.
    """

    valid: bool

    message: str | None = None

    failed_paragraph: str | None = None

    warnings: list[str] = field(
        default_factory=list,
    )



class ValidationCoordinator:
    """
    Central validation pipeline.

    Validates:

        Optimized Document
              |
              v
        Content Validation
              |
              v
        Style Validation
              |
              v
        Final Result


    Responsibilities:
        - Coordinate validators.
        - Compare original vs optimized.
        - Protect document integrity.

    Does not:
        - Modify document.
        - Rewrite content.
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


        # ----------------------------------
        # Validate planned rewrites only
        # ----------------------------------

        for rewrite in plan.rewrites:

            paragraph_id = (
                rewrite.paragraph_id
            )


            original_paragraph = (
                original_lookup.get(
                    paragraph_id
                )
            )


            optimized_paragraph = (
                optimized_lookup.get(
                    paragraph_id
                )
            )


            if (
                original_paragraph is None
                or optimized_paragraph is None
            ):

                return ValidationResult(

                    valid=False,

                    message=(
                        "Paragraph missing "
                        f"during validation: "
                        f"{paragraph_id}"
                    ),

                    failed_paragraph=(
                        paragraph_id
                    ),
                )


            # ----------------------------------
            # Content + Layout validation
            # ----------------------------------

            content_result = (
                ContentValidator.validate(
                    paragraph=original_paragraph,
                    optimized_text=(
                        optimized_paragraph.text
                    ),
                    constraints=None,
                )
            )


            if not content_result.valid:

                return ValidationResult(

                    valid=False,

                    message=(
                        content_result.message
                    ),

                    failed_paragraph=(
                        paragraph_id
                    ),
                )


            # ----------------------------------
            # Style preservation
            # ----------------------------------

            style_result = (
                StyleValidator.validate(
                    original=original_paragraph,
                    optimized=optimized_paragraph,
                )
            )


            if not style_result.valid:

                return ValidationResult(

                    valid=False,

                    message=(
                        style_result.message
                    ),

                    failed_paragraph=(
                        paragraph_id
                    ),
                )


        return ValidationResult(

            valid=True,

            message=None,

        )