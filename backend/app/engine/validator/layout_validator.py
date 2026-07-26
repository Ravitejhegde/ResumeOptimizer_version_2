from __future__ import annotations

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
    Validates optimized content against the
    planner-generated layout constraints.
    """

    @staticmethod
    def validate(
        constraints: LayoutConstraints,
        optimized_text: str,
    ) -> LayoutValidationResult:

        character_count = len(
            optimized_text
        )

        word_count = len(
            optimized_text.split()
        )

        estimated_lines = max(
            1,
            optimized_text.count("\n") + 1,
        )

        character_overflow = (
            character_count >
            constraints.max_characters
        )

        word_overflow = (
            word_count >
            constraints.max_words
        )

        line_overflow = (
            estimated_lines >
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
            )

        reasons = []

        if character_overflow:
            reasons.append(
                f"Characters {character_count}/{constraints.max_characters}"
            )

        if word_overflow:
            reasons.append(
                f"Words {word_count}/{constraints.max_words}"
            )

        if line_overflow:
            reasons.append(
                f"Lines {estimated_lines}/{constraints.max_lines}"
            )

        return LayoutValidationResult(
            valid=False,
            character_overflow=character_overflow,
            word_overflow=word_overflow,
            line_overflow=line_overflow,
            message=" | ".join(reasons),
        )