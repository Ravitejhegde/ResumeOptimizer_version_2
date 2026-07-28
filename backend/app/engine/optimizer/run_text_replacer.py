from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import (
    Paragraph,
)


class RunTextReplacer:
    """
    Safely replaces paragraph text while
    preserving formatting.
    """

    @staticmethod
    def apply(
        paragraph: Paragraph,
        text: str,
    ) -> Paragraph:

        if not paragraph.editable:
            return paragraph

        optimized = replace(
            paragraph,
        )

        if not optimized.runs:
            return optimized

        optimized.runs[0].text = text

        for run in optimized.runs[1:]:

            run.text = ""

        return optimized