"""
app.planner.goal.optimization_goal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the optimization objective.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationGoal:
    """
    High-level optimization objective.
    """

    current_role: str = ""

    target_role: str = ""

    objective: str = ""

    optimization_level: str = "minor"

    matched_roles: list[str] = field(
        default_factory=list
    )

    target_skills: list[str] = field(
        default_factory=list
    )

    target_technologies: list[str] = field(
        default_factory=list
    )

    notes: list[str] = field(
        default_factory=list
    )