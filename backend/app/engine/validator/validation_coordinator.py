from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.document import Document
from app.engine.validator.content_validator import (
    ContentValidator,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Overall validation result for an optimized document.
    """

    valid: bool

    message: str | None = None


class ValidationCoordinator:
    """
    Coordinates all validation stages.

    Pipeline

        Content
            ↓
        Layout
            ↓
        Style (future)
            ↓
        ATS (future)
    """

    def validate(
        self,
        original: Document,
        optimized: Document,
    ) -> ValidationResult:

        for original_paragraph, optimized_paragraph in zip(
            original.paragraphs,
            optimized.paragraphs,
        ):

            result = ContentValidator.validate(
                paragraph=original_paragraph,
                optimized_text=optimized_paragraph.text,
            )

            if not result.valid:

                return ValidationResult(
                    valid=False,
                    message=result.message,
                )

        return ValidationResult(
            valid=True,
        )