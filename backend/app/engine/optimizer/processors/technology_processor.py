from __future__ import annotations

from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


class TechnologyProcessor:
    """
    Applies technology promotion instructions
    to a paragraph.

    This class prepares the paragraph for AI.
    It NEVER calls AI directly.
    """

    # --------------------------------------------------

    def process(
        self,
        paragraph: Paragraph,
        rewrites: list[RewritePlan],
    ) -> tuple[
        Paragraph,
        list[str],
    ]:

        technologies: list[str] = []

        for rewrite in rewrites:

            if rewrite.action != "promote":

                continue

            technologies.append(
                rewrite.technology,
            )

        return (
            paragraph,
            technologies,
        )
