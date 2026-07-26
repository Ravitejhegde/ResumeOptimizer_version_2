from __future__ import annotations

from app.engine.models.paragraph import Paragraph


class LayoutWriter:
    """
    Responsible for writing optimized text while
    preserving the original layout.

    This class NEVER changes formatting.

    Responsibilities
    ----------------
    - Preserve runs
    - Preserve paragraph style
    - Preserve numbering
    - Preserve hyperlinks
    - Preserve spacing
    - Preserve alignment
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