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
    Build the optimization instructions for AI.

    The Planner has already made the optimization
    decisions. The AI only executes those decisions
    by rewriting existing resume paragraphs.
    """

    lines: list[str] = []

    lines.append("OPTIMIZATION PLAN")

    # ----------------------------------
    # Goal
    # ----------------------------------

    if blueprint.goal:
        lines.append("")
        lines.append("GOAL")

        lines.append(
            f"Objective: {blueprint.goal.objective}"
        )

        lines.append(
            f"Target Role: {blueprint.goal.target_role}"
        )

    # ----------------------------------
    # Decision
    # ----------------------------------

    if blueprint.decision:
        lines.append("")
        lines.append("DECISION")

        lines.append(
            f"Strategy: {blueprint.decision.strategy}"
        )

        lines.append(
            f"Optimization Level: "
            f"{blueprint.decision.optimization_level}"
        )

    # ----------------------------------
    # Optimization Knowledge
    # ----------------------------------

    if blueprint.knowledge:
        knowledge = blueprint.knowledge

        lines.append("")
        lines.append("OPTIMIZATION KNOWLEDGE")

        if knowledge.role_name:
            lines.append(
                f"Target Role: {knowledge.role_name}"
            )

        if knowledge.matched_skills:
            lines.append("Matched Skills:")

            for skill in knowledge.matched_skills:
                lines.append(
                    f"- {skill}"
                )

        if knowledge.selected_missing_skills:
            lines.append(
                "User-Selected Missing Skills:"
            )

            for skill in knowledge.selected_missing_skills:
                lines.append(
                    f"- {skill}"
                )

        if knowledge.optimization_skills:
            lines.append("")
            lines.append(
                "Optimization Skills:"
            )

            for skill in knowledge.optimization_skills:
                status: list[str] = []

                if skill.matched:
                    status.append("matched")

                if skill.user_selected:
                    status.append("user-selected")

                status_text = (
                    ", ".join(status)
                    if status
                    else "not authorized"
                )

                lines.append(
                    f"- {skill.name} "
                    f"[{status_text}] "
                    f"| category="
                    f"{skill.presentation_category} "
                    f"| relevance="
                    f"{skill.role_relevance}"
                )

    # ----------------------------------
    # Priority Plan
    # ----------------------------------

    if blueprint.priorities.items:
        lines.append("")
        lines.append("PRIORITIES")

        for item in blueprint.priorities.items:
            lines.append(
                f"- {item.id}"
            )

            lines.append(
                f"  Type: {item.type}"
            )

            lines.append(
                f"  Priority: {item.priority_level}"
            )

            lines.append(
                f"  Score: {item.priority_score}"
            )

            if item.description:
                lines.append(
                    f"  Description: {item.description}"
                )

            if item.reason:
                lines.append(
                    f"  Reason: {item.reason}"
                )

            if item.affected_sections:
                lines.append(
                    "  Sections: "
                    + ", ".join(
                        item.affected_sections
                    )
                )

    # ----------------------------------
    # Evidence
    # ----------------------------------

    if blueprint.evidence.items:
        lines.append("")
        lines.append("EVIDENCE")

        for item in blueprint.evidence.items:
            lines.append(
                f"- {item.id}"
            )

            lines.append(
                f"  Supported: {item.supported}"
            )

            if item.reasoning:
                lines.append(
                    "  Reasoning: "
                    + " | ".join(item.reasoning)
                )

            if item.recommended_action:
                lines.append(
                    f"  Recommended Action: "
                    f"{item.recommended_action}"
                )

    # ----------------------------------
    # Section Plan
    # ----------------------------------

    if blueprint.section_plan.sections:
        lines.append("")
        lines.append("SECTION PLAN")

        for (
            section,
            item_ids,
        ) in blueprint.section_plan.sections.items():

            lines.append(
                f"- {section}: "
                + ", ".join(item_ids)
            )

    if blueprint.section_plan.untouched_sections:
        lines.append(
            "Untouched Sections: "
            + ", ".join(
                blueprint.section_plan.untouched_sections
            )
        )

    if blueprint.section_plan.paragraph_ids:
        lines.append("")
        lines.append("AUTHORIZED PARAGRAPHS")

        for (
            section,
            paragraph_ids,
        ) in blueprint.section_plan.paragraph_ids.items():

            lines.append(
                f"- {section}: "
                + ", ".join(paragraph_ids)
            )

    # ----------------------------------
    # Rewrite Plan
    # ----------------------------------

    if blueprint.rewrite_plan.section_levels:
        lines.append("")
        lines.append("REWRITE PLAN")

        for (
            section,
            level,
        ) in (
            blueprint.rewrite_plan
            .section_levels
            .items()
        ):
            lines.append(
                f"- {section}: {level}"
            )

            actions = (
                blueprint.rewrite_plan
                .section_actions
                .get(section, [])
            )

            for action in actions:
                lines.append(
                    f"  Action: {action}"
                )

    if blueprint.rewrite_plan.global_strategy:
        lines.append(
            "Global Strategy: "
            + blueprint.rewrite_plan.global_strategy
        )

    # ----------------------------------
    # Budget
    # ----------------------------------

    if blueprint.budget:
        budget = blueprint.budget

        lines.append("")
        lines.append("CONTENT BUDGET")

        lines.append(
            f"Total Tokens: {budget.total_tokens}"
        )

        lines.append(
            f"Maximum Priority Items: "
            f"{budget.max_priority_items}"
        )

        lines.append(
            f"Rewrite Intensity: "
            f"{budget.rewrite_intensity}"
        )

        if budget.section_budgets:
            lines.append(
                "Section Budgets:"
            )

            for section_budget in budget.section_budgets:
                lines.append(
                    f"- {section_budget.section}: "
                    f"{section_budget.estimated_tokens} "
                    f"tokens "
                    f"({section_budget.percentage}%)"
                )

        if budget.constraints:
            lines.append(
                "Budget Constraints:"
            )

            for constraint in budget.constraints:
                lines.append(
                    f"- {constraint}"
                )

    # ----------------------------------
    # Execution Rules
    # ----------------------------------

    lines.append("")
    lines.append("EXECUTION RULES")

    lines.append(
        "1. Rewrite only existing resume paragraphs."
    )

    lines.append(
        "2. Preserve every paragraph ID exactly."
    )

    lines.append(
        "3. Return only paragraphs that actually "
        "require optimization."
    )

    lines.append(
        "4. Strengthen matched skills only when "
        "supported by the existing resume."
    )

    lines.append(
        "5. Incorporate user-selected missing skills "
        "only when the Planner targets them."
    )

    lines.append(
        "6. User-selected skills authorize keyword "
        "incorporation, but do not authorize invented "
        "experience, projects, achievements, "
        "responsibilities, certifications, employment "
        "history, or measurable results."
    )

    lines.append(
        "7. Do not add missing skills that were not "
        "matched or explicitly selected by the user."
    )

    lines.append(
        "8. Do not modify protected or untouched sections."
    )

    lines.append(
        "9. Preserve the factual meaning of the "
        "original resume."
    )

    lines.append(
        "10. Improve wording, clarity, ATS alignment, "
        "and keyword usage without fabricating facts."
    )

    lines.append(
        "11. Follow the section plan, rewrite plan, "
        "optimization knowledge, evidence, and budget."
    )

    lines.append(
        "12. Keep optimized text concise, truthful, "
        "ATS-friendly, and professionally written."
    )

    return "\n".join(lines)
