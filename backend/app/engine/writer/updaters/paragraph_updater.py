from __future__ import annotations

from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


class ParagraphUpdater:
    """
    Updates paragraph content while preserving
    paragraph-level formatting.
    """

    # --------------------------------------------------

    def update(
        self,
        paragraph: Paragraph,
        rewrite: RewriteResult,
    ) -> Paragraph:

        if not paragraph.runs:

            return paragraph

        paragraph.runs[0].text = (
            rewrite.optimized_text
        )

        for run in paragraph.runs[1:]:

            run.text = ""

        return paragraph
