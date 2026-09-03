"""
app.planner.budget.optimization_budget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the content and token budget
prepared by the Planner.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionBudget:
    """
    Budget allocated to a single resume section.
    """

    section: str = ""
    percentage: float = 0.0
    estimated_tokens: int = 0
    priority_count: int = 0


@dataclass(slots=True)
class OptimizationBudget:
    """
    Complete optimization budget produced by
    the Budget Maker.
    """

    total_tokens: int = 0

    section_budgets: list[SectionBudget] = field(
        default_factory=list
    )

    max_priority_items: int = 0

    rewrite_intensity: str = "moderate"

    constraints: list[str] = field(
        default_factory=list
    )