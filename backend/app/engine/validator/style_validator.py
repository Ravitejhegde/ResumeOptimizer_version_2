from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.paragraph import Paragraph


@dataclass(slots=True, frozen=True)
class StyleValidationResult:
    """
    Result of style validation.
    """

    valid: bool

    message: str | None = None


class StyleValidator:
    """
    Validates that paragraph styling has been
    preserved after optimization.

    Responsibilities
    ----------------
    • Validate formatting preservation
    • Validate run structure
    • Never modify the document

    Future checks
    -------------
    • Font family
    • Font size
    • Bold
    • Italic
    • Underline
    • Colors
    • Highlight
    • Paragraph style
    """

    @staticmethod
    def validate(
        original: Paragraph,
        optimized: Paragraph,
    ) -> StyleValidationResult:

        return StyleValidationResult(
            valid=True,
        )