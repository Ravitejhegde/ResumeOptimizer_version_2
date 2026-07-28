from __future__ import annotations

from app.engine.models.intelligence.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)
from app.engine.models.planner.section_plan import (
    SectionPlan,
)


class OptimizationPlanBuilder:
    """
    Converts an OptimizationStrategy into an
    executable OptimizationPlan.
    """

    # --------------------------------------------------

    def build(
        self,
        strategy: OptimizationStrategy,
    ) -> OptimizationPlan:

        plan = OptimizationPlan()

        for decision in (
            strategy.promotion_plan.decisions
            if strategy.promotion_plan
            else []
        ):

            plan.sections.append(

                SectionPlan(

                    section=decision.section,

                    priority=decision.priority,

                    technologies=[
                        decision.technology,
                    ],

                )

            )

        return plan
