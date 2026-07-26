from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.paragraph import (
    Paragraph,
)
from app.engine.planner.layout_budget_planner import (
    LayoutConstraints,
)
from app.engine.validator.layout_validator import (
    LayoutValidationResult,
    LayoutValidator,
)


@dataclass(slots=True, frozen=True)
class ContentValidationResult:
    """
    Result of content validation.
    """

    valid: bool

    message: str |None = None

    layout_result: LayoutValidationResult | None = None


class ContentValidator:
    """
    Validates optimized paragraph content.

    Responsibilities
    ----------------
    - Ensure paragraph is editable
    - Ensure optimized text is not empty
    - Delegate layout validation
    """

    @staticmethod
    def validate(
        paragraph: Paragraph,
        optimized_text: str,
        constraints: LayoutConstraints | None,
    ) -> ContentValidationResult:

        if not paragraph.editable:
            return ContentValidationResult(
                valid=False,
                message="Paragraph is locked.",
            )

        if not optimized_text.strip():

            return ContentValidationResult(
        valid=False,
        message=(
            f"Optimized text is empty "
            f"(Paragraph: {paragraph.id})"
        ),
    )

        if constraints is not None:

            layout_result = LayoutValidator.validate(
                constraints=constraints,
                optimized_text=optimized_text,
            )

            if not layout_result.valid:
                return ContentValidationResult(
                    valid=False,
                    message=layout_result.message,
                    layout_result=layout_result,
                )

        return ContentValidationResult(
            valid=True,
            message=None,
            layout_result=None,
        )