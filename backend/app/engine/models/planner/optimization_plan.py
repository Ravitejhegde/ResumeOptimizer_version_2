from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)
from app.engine.models.planner.section_plan import (
    SectionPlan,
)


@dataclass(slots=True)
class OptimizationPlan:
    """
    Final execution plan produced by
    the Planner.
    """

    sections: list[
        SectionPlan
    ] = field(
        default_factory=list,
    )

    rewrites: list[
        RewritePlan
    ] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )
