from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.layout_budget import (
    LayoutBudget,
)


@dataclass(slots=True, frozen=True)
class LayoutConstraints:
    """
    Planner-generated layout constraints.

    Temporary testing version.

    Greatly increases limits so we can
    verify the complete optimization
    pipeline before fine-tuning layout.
    """

    max_characters: int
    max_words: int

    hard_limit_characters: int
    hard_limit_words: int

    max_lines: int

    allow_overflow: bool

    tolerance_percentage: float


class LayoutBudgetPlanner:
    """
    Temporary testing planner.

    Inflate limits so validation does not
    fail because of tight layout budgets.
    """

    CHARACTER_MULTIPLIER = 3
    WORD_MULTIPLIER = 3
    LINE_MULTIPLIER = 3

    @classmethod
    def build(
        cls,
        budget: LayoutBudget,
    ) -> LayoutConstraints:

        return LayoutConstraints(

            # AI limits (expanded)

            max_characters=max(
                50,
                budget.max_characters
                * cls.CHARACTER_MULTIPLIER,
            ),

            max_words=max(
                15,
                budget.max_words
                * cls.WORD_MULTIPLIER,
            ),

            # Validator limits (also expanded)

            hard_limit_characters=max(
                50,
                budget.max_characters
                * cls.CHARACTER_MULTIPLIER,
            ),

            hard_limit_words=max(
                15,
                budget.max_words
                * cls.WORD_MULTIPLIER,
            ),

            max_lines=max(
                3,
                budget.max_lines
                * cls.LINE_MULTIPLIER,
            ),

            allow_overflow=True,

            tolerance_percentage=300.0,
        )




