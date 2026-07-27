from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.planner.plan import (
    OptimizationPlan,
)


class ParagraphSelector:
    """
    Selects which paragraphs should be
    sent to AI for rewriting.

    Planner already decided WHICH paragraphs
    are eligible.

    This class simply converts the plan into
    actual paragraph objects.
    """

    @staticmethod
    def select(
        document: Document,
        plan: OptimizationPlan,
    ) -> list:

        paragraphs = []

        for paragraph in document.paragraphs:

            if (
                paragraph.id
                not in plan.rewrite_paragraph_ids
            ):
                continue

            paragraphs.append(
                paragraph
            )

        return paragraphs




