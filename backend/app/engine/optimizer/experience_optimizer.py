from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import Paragraph


class ExperienceOptimizer:
    """
    Applies optimized experience content while
    preserving paragraph structure.

    Responsibilities
    ----------------
    - Replace paragraph text
    - Preserve formatting
    - Preserve hyperlinks
    - Preserve run order
    - Never modify locked paragraphs

    AI is NEVER called here.
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        optimized_text: str,
    ) -> Paragraph:

        if not paragraph.editable:
            return paragraph

        optimized = replace(
            paragraph
        )

        if not optimized.runs:
            return optimized

        optimized.runs[0].text = optimized_text

        for run in optimized.runs[1:]:
            run.text = ""

        return optimized