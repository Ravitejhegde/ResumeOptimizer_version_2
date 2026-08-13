"""
app.optimizer.prompts.planner_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the optimization plan prompt.
"""

from __future__ import annotations

from app.planner.blueprint.optimization_blueprint import (
    OptimizationBlueprint,
)


def build_planner_prompt(
    blueprint: OptimizationBlueprint,
) -> str:
    """
    Build the planner instructions for AI.
    """

    lines: list[str] = []

    lines.append("OPTIMIZATION PLAN")

    if blueprint.goal:
        lines.append(
            f"Goal: {blueprint.goal}"
        )

    if blueprint.decision:
        lines.append(
            f"Decision: {blueprint.decision}"
        )

    if blueprint.target_sections:
        lines.append(
            "Target Sections:"
        )

        for section in blueprint.target_sections:
            lines.append(
                f"- {section}"
            )

    if blueprint.execution_order:
        lines.append(
            "Execution Order:"
        )

        for step in blueprint.execution_order:
            lines.append(
                f"- {step}"
            )

    if blueprint.rewrite_strategy:
        lines.append(
            f"Rewrite Strategy: {blueprint.rewrite_strategy}"
        )

    if blueprint.safety_rules:
        lines.append(
            "Safety Rules:"
        )

        for rule in blueprint.safety_rules:
            lines.append(
                f"- {rule}"
            )

    lines.append("")
    lines.append(
        "Follow this optimization plan exactly."
    )

    lines.append(
        "Do not optimize sections outside this plan."
    )

    return "\n".join(lines)