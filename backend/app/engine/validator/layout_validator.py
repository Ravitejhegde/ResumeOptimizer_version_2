from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.layout_budget import LayoutBudget


@dataclass(slots=True, frozen=True)
class LayoutValidationResult:
    valid: bool

    character_overflow: bool

    word_overflow: bool

    line_overflow: bool

    message: str | None = None


class LayoutValidator:
    """
    Validates that optimized content stays within
    the original layout budget.
    """

    @staticmethod
    def validate(
        budget: LayoutBudget,
        optimized_text: str,
    ) -> LayoutValidationResult:

        character_count = len(optimized_text)

        word_count = len(optimized_text.split())

        estimated_lines = max(
            1,
            optimized_text.count("\n") + 1,
        )

        character_overflow = (
            character_count > budget.max_characters
        )

        word_overflow = (
            word_count > budget.max_words
        )

        line_overflow = (
            estimated_lines > budget.max_lines
        )

        valid = not (
            character_overflow
            or word_overflow
            or line_overflow
        )

        return LayoutValidationResult(
            valid=valid,
            character_overflow=character_overflow,
            word_overflow=word_overflow,
            line_overflow=line_overflow,
            message=None if valid else "Layout budget exceeded.",
        )