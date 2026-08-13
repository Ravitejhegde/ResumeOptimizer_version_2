"""
app.planner.rewrite.rewrite_planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines how aggressively each section should be rewritten.
"""

from __future__ import annotations

from app.planner.goal.optimization_goal import (
    OptimizationGoal,
)
from app.planner.rewrite.rewrite_plan import (
    RewritePlan,
)
from app.planner.section.section_plan import (
    SectionPlan,
)


class RewritePlanner:
    """
    Builds rewrite instructions for each section.
    """

    def build(
        self,
        goal: OptimizationGoal,
        sections: SectionPlan,
    ) -> RewritePlan:
        """
        Build a rewrite plan based on the optimization goal.
        """

        plan = RewritePlan()

        plan.global_strategy = goal.optimization_level

        for section, items in sections.sections.items():

            if goal.optimization_level == "minor":
                level = "keyword_enhancement"

            elif goal.optimization_level == "moderate":
                level = "bullet_improvement"

            else:
                level = "full_rewrite"

            plan.section_levels[section] = level

            plan.section_actions[section] = list(items)

            plan.reasoning[section] = (
                f"{level} selected based on "
                f"{goal.optimization_level} optimization."
            )

        return plan