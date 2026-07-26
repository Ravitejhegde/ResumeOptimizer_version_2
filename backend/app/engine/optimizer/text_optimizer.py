from __future__ import annotations

from app.engine.models.paragraph import (
    Paragraph,
)


class TextOptimizer:
    """
    Applies AI-generated text to an existing paragraph.

    Responsibilities
    ----------------
    - Never calls AI
    - Never changes formatting
    - Never changes runs except their text
    - Updates the paragraph in-place
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        optimized_text: str,
    ) -> Paragraph:

        if not paragraph.runs:
            return paragraph

        paragraph.runs[0].text = optimized_text

        for run in paragraph.runs[1:]:

            run.text = ""

        return paragraph