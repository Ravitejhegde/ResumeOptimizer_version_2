"""
app.planner.prompt.prompt_planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the prompt execution strategy from
the optimization blueprint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.planner.prompt.prompt_plan import (
    PromptPlan,
)

if TYPE_CHECKING:
    from app.planner.blueprint.optimization_blueprint import (
        OptimizationBlueprint,
    )


class PromptPlanner:
    """
    Converts planning decisions into a single
    AI prompt execution strategy.

    The actual final prompt is assembled later
    by Optimizer PromptBuilder.
    """

    def build(
        self,
        blueprint: OptimizationBlueprint,
    ) -> PromptPlan:
        """
        Build a single-prompt execution plan.
        """

        plan = PromptPlan()

        sections = list(
            blueprint.rewrite_plan.section_levels.keys()
        )

        if sections:
            plan.prompts.append(
                "Execute the complete optimization plan "
                "in a single AI generation."
            )

            plan.prompts.append(
                "Target sections: "
                + ", ".join(sections)
            )

        plan.prompt_count = 1 if plan.prompts else 0

        plan.estimated_tokens = sum(
            len(prompt.split())
            for prompt in plan.prompts
        )

        return plan