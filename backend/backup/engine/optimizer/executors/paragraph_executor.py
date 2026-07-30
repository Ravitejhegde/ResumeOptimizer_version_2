from __future__ import annotations

from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


class ParagraphExecutor:
    """
    Executes optimization on a single paragraph.
    """

    # --------------------------------------------------

    def execute(
        self,
        paragraph: Paragraph,
        rewrites: list[RewritePlan],
    ) -> tuple[Paragraph, list[RewritePlan]]:

        applicable = [

            rewrite

            for rewrite in rewrites

            if rewrite.paragraph_id == paragraph.id

        ]

        return (
            paragraph,
            applicable,
        )
