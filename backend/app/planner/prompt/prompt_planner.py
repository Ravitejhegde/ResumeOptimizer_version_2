"""
app.planner.prompt.prompt_planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds AI prompts from the optimization blueprint.
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
    Converts planning decisions into AI prompts.
    """

    def build(
        self,
        blueprint: OptimizationBlueprint,
    ) -> PromptPlan:
        """
        Build AI prompts from the optimization blueprint.
        """

        plan = PromptPlan()

        for (
            section,
            level,
        ) in blueprint.rewrite_plan.section_levels.items():

            prompt = (
                f"Rewrite the '{section}' section.\n"
                f"Rewrite level: {level}\n"
                f"Goal: {blueprint.goal.objective}\n"
                f"Target role: {blueprint.goal.target_role}\n"
                f"Only strengthen supported evidence.\n"
                f"Never invent experience.\n"
            )

            plan.prompts.append(
                prompt
            )

        plan.prompt_count = len(
            plan.prompts
        )

        plan.estimated_tokens = sum(
            len(prompt.split())
            for prompt in plan.prompts
        )

        return plan