from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class TechnologyTarget:
    """
    One technology that should be promoted.
    """

    technology: str

    category: str

    score: int

    action: str

    section: str

    paragraph_id: str

    reason: str


@dataclass(slots=True)
class OptimizationStrategy:
    """
    Final optimization strategy shared across
    Analyzer → Planner → Optimizer → AI.

    This object contains only business
    decisions, never implementation logic.
    """

    role: str = ""

    role_family: str = ""

    categories: dict[
        str,
        list[str],
    ] = field(default_factory=dict)

    targets: list[
        TechnologyTarget
    ] = field(default_factory=list)

    summary_targets: list[str] = field(
        default_factory=list
    )

    experience_targets: list[str] = field(
        default_factory=list
    )

    project_targets: list[str] = field(
        default_factory=list
    )

    skills_targets: list[str] = field(
        default_factory=list
    )

    ignored: list[str] = field(
        default_factory=list
    )

    metadata: dict[
        str,
        object,
    ] = field(default_factory=dict)




