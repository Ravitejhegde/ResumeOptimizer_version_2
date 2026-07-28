from __future__ import annotations

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)
from app.engine.models.planner.section_plan import (
    SectionPlan,
)


class SectionPlanBuilder:
    """
    Groups optimization work by section.
    """

    # --------------------------------------------------

    def build(
        self,
        plan: OptimizationPlan,
    ) -> OptimizationPlan:

        merged: dict[
            str,
            SectionPlan,
        ] = {}

        for section in plan.sections:

            if section.section not in merged:

                merged[
                    section.section
                ] = SectionPlan(

                    section=section.section,

                    editable=section.editable,

                    priority=section.priority,

                )

            merged[
                section.section
            ].technologies.extend(
                section.technologies,
            )

            merged[
                section.section
            ].paragraphs.extend(
                section.paragraphs,
            )

            merged[
                section.section
            ].notes.extend(
                section.notes,
            )

        plan.sections = list(
            merged.values(),
        )

        return plan
