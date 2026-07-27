from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import (
    Paragraph,
)


class LayoutWriter:
    """
    Applies optimized text to an engine Paragraph
    while preserving paragraph structure.

    Responsibilities
    ----------------
    - Preserve paragraph formatting
    - Preserve run ordering
    - Preserve paragraph metadata

    Never writes to DOCX directly.
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        optimized_text: str,
    ) -> Paragraph:

        updated = replace(paragraph)

        if not updated.runs:
            return updated

        updated.runs[0].text = optimized_text

        for run in updated.runs[1:]:
            run.text = ""

        return updated




