from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document.paragraph import (
    Paragraph,
)


@dataclass(slots=True, frozen=True)
class StyleValidationResult:
    """
    Result of style preservation validation.
    """

    valid: bool

    message: str | None = None



class StyleValidator:
    """
    Validates formatting preservation after optimization.

    Responsibilities:
        - Compare original paragraph formatting.
        - Detect style corruption.
        - Protect document appearance.

    Does not:
        - Modify paragraph.
        - Fix formatting.
        - Rewrite content.
    """


    @staticmethod
    def validate(
        original: Paragraph,
        optimized: Paragraph,
    ) -> StyleValidationResult:
        """
        Compare original and optimized paragraph styles.
        """


        if original is None or optimized is None:

            return StyleValidationResult(

                valid=False,

                message=(
                    "Paragraph cannot be None."
                ),
            )


        # ----------------------------------
        # Paragraph style
        # ----------------------------------

        if (
            original.style_name
            !=
            optimized.style_name
        ):

            return StyleValidationResult(

                valid=False,

                message=(
                    "Paragraph style changed."
                ),
            )


        # ----------------------------------
        # Run structure
        # ----------------------------------

        if len(original.runs) != len(
            optimized.runs
        ):

            return StyleValidationResult(

                valid=False,

                message=(
                    "Run structure changed."
                ),
            )


        # ----------------------------------
        # Character formatting
        # ----------------------------------

        for index, (
            original_run,
            optimized_run,
        ) in enumerate(
            zip(
                original.runs,
                optimized.runs,
            )
        ):

            result = (
                StyleValidator
                ._compare_run_style(
                    original_run.style,
                    optimized_run.style,
                )
            )


            if not result:

                return StyleValidationResult(

                    valid=False,

                    message=(
                        f"Formatting changed "
                        f"in run {index}."
                    ),
                )


        return StyleValidationResult(

            valid=True,

            message=None,

        )


    @staticmethod
    def _compare_run_style(
        original,
        optimized,
    ) -> bool:
        """
        Compare immutable TextStyle objects.
        """

        return (

            original.font_name
            ==
            optimized.font_name

            and

            original.font_size
            ==
            optimized.font_size

            and

            original.bold
            ==
            optimized.bold

            and

            original.italic
            ==
            optimized.italic

            and

            original.underline
            ==
            optimized.underline

            and

            original.strike
            ==
            optimized.strike

            and

            original.subscript
            ==
            optimized.subscript

            and

            original.superscript
            ==
            optimized.superscript

            and

            original.color
            ==
            optimized.color

            and

            original.highlight
            ==
            optimized.highlight

        )