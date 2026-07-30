from __future__ import annotations

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)
from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


class RewritePlanBuilder:
    """
    Builds paragraph-level rewrite instructions
    from the section plans.
    """

    # --------------------------------------------------

    def build(
        self,
        plan: OptimizationPlan,
    ) -> OptimizationPlan:

        rewrites: list[
            RewritePlan
        ] = []

        for section in plan.sections:

            for paragraph_id in section.paragraphs:

                for technology in section.technologies:

                    rewrites.append(

                        RewritePlan(

                            paragraph_id=paragraph_id,

                            section=section.section,

                            technology=technology,

                            action="promote",

                            priority=section.priority,

                            reason="Technology promotion",

                        )

                    )

        plan.rewrites = rewrites

        return plan
