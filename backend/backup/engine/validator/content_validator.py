from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document.paragraph import (
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
    Result of paragraph content validation.
    """

    valid: bool

    message: str | None = None

    layout_result: LayoutValidationResult | None = None



class ContentValidator:
    """
    Validates optimized paragraph content.

    Responsibilities:
        - Check paragraph editability.
        - Check optimized text validity.
        - Prevent unsafe content expansion.
        - Delegate layout validation.

    Does not:
        - Rewrite content.
        - Compare skills.
        - Apply optimization rules.
    """


    MAX_EXPANSION_RATIO = 3.0


    @staticmethod
    def validate(
        paragraph: Paragraph,
        optimized_text: str,
        constraints: LayoutConstraints | None = None,
    ) -> ContentValidationResult:
        """
        Validate optimized paragraph output.
        """


        # ----------------------------------
        # Editable check
        # ----------------------------------

        if not paragraph.editable:

            return ContentValidationResult(

                valid=False,

                message=(
                    "Paragraph is locked."
                ),
            )


        # ----------------------------------
        # Empty content check
        # ----------------------------------

        cleaned_text = (
            optimized_text.strip()
        )


        if not cleaned_text:

            return ContentValidationResult(

                valid=False,

                message=(
                    f"Optimized text is empty "
                    f"(Paragraph: {paragraph.id})"
                ),
            )


        # ----------------------------------
        # Expansion safety
        # ----------------------------------

        original_length = len(
            paragraph.text.strip()
        )

        optimized_length = len(
            cleaned_text
        )


        if (
            original_length > 0
            and optimized_length
            >
            original_length
            *
            ContentValidator.MAX_EXPANSION_RATIO
        ):

            return ContentValidationResult(

                valid=False,

                message=(
                    "Optimized text exceeds "
                    "allowed expansion limit."
                ),
            )


        # ----------------------------------
        # Layout validation
        # ----------------------------------

        if constraints is not None:

            layout_result = (
                LayoutValidator.validate(
                    constraints=constraints,
                    optimized_text=cleaned_text,
                )
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

                layout_result=layout_result,
            )


        # ----------------------------------
        # Valid
        # ----------------------------------

        return ContentValidationResult(

            valid=True,

            message=None,

            layout_result=None,
        )