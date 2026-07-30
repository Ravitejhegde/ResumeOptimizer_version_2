from __future__ import annotations

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)


class BudgetAllocator:
    """
    Assigns paragraph budget to each
    section plan.
    """

    # --------------------------------------------------

    def allocate(
        self,
        plan: OptimizationPlan,
        document: Document,
    ) -> OptimizationPlan:

        paragraphs_by_section = {}

        for paragraph in document.paragraphs:

            if paragraph.section is None:
                continue

            paragraphs_by_section.setdefault(
                paragraph.section,
                [],
            ).append(
                paragraph.id,
            )

        for section in plan.sections:

            section.paragraphs = (
                paragraphs_by_section.get(
                    section.section,
                    [],
                )
            )

        return plan
