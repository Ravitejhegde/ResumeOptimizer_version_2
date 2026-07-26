from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import Paragraph


class TextOptimizer:
    """
    Applies rewritten text to a paragraph.

    This class NEVER calls AI.

    It simply applies already-approved text while
    preserving every formatting object.
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        optimized_text: str,
    ) -> Paragraph:

        new_paragraph = replace(
            paragraph
        )

        if not new_paragraph.runs:

            return new_paragraph

        new_paragraph.runs[0].text = optimized_text

        for run in new_paragraph.runs[1:]:

            run.text = ""

        return new_paragraph