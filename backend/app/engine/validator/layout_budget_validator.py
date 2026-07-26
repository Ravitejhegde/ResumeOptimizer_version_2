from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.layout_budget import LayoutBudget


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


class LayoutBudgetValidator:
    """
    Validates whether optimized content stays
    within the original layout budget.
    """

    @staticmethod
    def validate(
        budget: LayoutBudget | None,
        optimized_text: str,
    ) -> LayoutValidationResult:

        # If no layout budget exists, validation succeeds.
        if budget is None:
            return LayoutValidationResult(
                valid=True,
                character_overflow=False,
                word_overflow=False,
                line_overflow=False,
                message=None,
            )

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
            message=(
                None
                if valid
                else "Layout budget exceeded."
            ),
        )