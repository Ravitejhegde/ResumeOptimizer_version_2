"""
app.planner.budget.budget_maker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the optimization budget from Planner decisions.
"""

from __future__ import annotations

from app.planner.budget.optimization_budget import (
    OptimizationBudget,
    SectionBudget,
)
from app.planner.decision.optimization_decision import (
    OptimizationDecision,
)
from app.planner.priority.priority_plan import (
    PriorityPlan,
)
from app.planner.rewrite.rewrite_plan import (
    RewritePlan,
)
from app.planner.section.section_plan import (
    SectionPlan,
)


class BudgetMaker:
    """
    Creates a deterministic content and token budget
    for the optimization process.
    """

    _BASE_TOKENS = {
        "minor": 800,
        "moderate": 1200,
        "major": 1800,
        "aggressive": 2400,
    }

    _SECTION_WEIGHTS = {
        "summary": 15.0,
        "experience": 40.0,
        "projects": 25.0,
        "skills": 20.0,
        "achievements": 15.0,
        "publications": 15.0,
    }

    def build(
        self,
        decision: OptimizationDecision,
        priorities: PriorityPlan,
        sections: SectionPlan,
        rewrite: RewritePlan,
    ) -> OptimizationBudget:
        """
        Build an optimization budget from existing
        Planner decisions.
        """

        level = decision.optimization_level or "moderate"

        total_tokens = self._BASE_TOKENS.get(
            level,
            self._BASE_TOKENS["moderate"],
        )

        active_sections = list(
            sections.sections.keys()
        )

        if not active_sections:
            active_sections = ["skills"]

        weights = {
            section: self._SECTION_WEIGHTS.get(
                section,
                10.0,
            )
            for section in active_sections
        }

        total_weight = sum(weights.values())

        section_budgets: list[SectionBudget] = []

        for section in active_sections:
            percentage = (
                weights[section] / total_weight
            ) * 100.0

            allocated_tokens = round(
                total_tokens * percentage / 100.0
            )

            priority_count = len(
                sections.sections.get(
                    section,
                    [],
                )
            )

            section_budgets.append(
                SectionBudget(
                    section=section,
                    percentage=round(
                        percentage,
                        2,
                    ),
                    estimated_tokens=allocated_tokens,
                    priority_count=priority_count,
                )
            )

        max_priority_items = len(
            priorities.items
        )

        constraints = [
            "Preserve original resume structure.",
            "Do not invent unsupported experience.",
            "User-selected missing skills may be incorporated.",
            "Respect section-level rewrite strategy.",
        ]

        return OptimizationBudget(
            total_tokens=total_tokens,
            section_budgets=section_budgets,
            max_priority_items=max_priority_items,
            rewrite_intensity=level,
            constraints=constraints,
        )