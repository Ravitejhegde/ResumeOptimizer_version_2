from __future__ import annotations

import math

from dataclasses import dataclass

from app.engine.planner.layout_budget_planner import (
    LayoutConstraints,
)


@dataclass(slots=True, frozen=True)
class LayoutValidationResult:
    """
    Result of layout validation.
    """

    valid: bool

    character_overflow: bool

    word_overflow: bool

    line_overflow: bool

    message: str | None = None



class LayoutValidator:
    """
    Validates optimized content against
    document layout constraints.

    The validator protects:
        - page length
        - paragraph capacity
        - original formatting budget

    It never modifies content.
    """


    DEFAULT_CHARACTERS_PER_LINE = 80


    @staticmethod
    def validate(
        constraints: LayoutConstraints,
        optimized_text: str,
    ) -> LayoutValidationResult:
        """
        Validate optimized text size.
        """

        if constraints is None:

            raise ValueError(
                "Layout constraints required."
            )


        text = (
            optimized_text.strip()
        )


        character_count = len(
            text
        )

        word_count = len(
            text.split()
        )

        estimated_lines = (
            LayoutValidator._estimate_lines(
                text
            )
        )


        # ----------------------------------
        # Compare against hard limits
        # ----------------------------------

        character_overflow = (
            character_count
            >
            constraints.hard_limit_characters
        )


        word_overflow = (
            word_count
            >
            constraints.hard_limit_words
        )


        line_overflow = (
            estimated_lines
            >
            constraints.max_lines
        )


        valid = not (
            character_overflow
            or word_overflow
            or line_overflow
        )


        if valid:

            return LayoutValidationResult(

                valid=True,

                character_overflow=False,

                word_overflow=False,

                line_overflow=False,

                message=None,
            )


        reasons: list[str] = []


        if character_overflow:

            reasons.append(
                (
                    "Character overflow: "
                    f"{character_count}/"
                    f"{constraints.hard_limit_characters}"
                )
            )


        if word_overflow:

            reasons.append(
                (
                    "Word overflow: "
                    f"{word_count}/"
                    f"{constraints.hard_limit_words}"
                )
            )


        if line_overflow:

            reasons.append(
                (
                    "Line overflow: "
                    f"{estimated_lines}/"
                    f"{constraints.max_lines}"
                )
            )


        return LayoutValidationResult(

            valid=False,

            character_overflow=character_overflow,

            word_overflow=word_overflow,

            line_overflow=line_overflow,

            message=" | ".join(reasons),

        )


    @staticmethod
    def _estimate_lines(
        text: str,
    ) -> int:
        """
        Estimate rendered line count.

        This is a lightweight approximation.
        Final DOCX rendering validation belongs
        to Writer validation.
        """

        if not text:

            return 1


        explicit_lines = (
            text.count("\n") + 1
        )


        calculated_lines = math.ceil(
            len(text)
            /
            LayoutValidator.DEFAULT_CHARACTERS_PER_LINE
        )


        return max(
            explicit_lines,
            calculated_lines,
            1,
        )