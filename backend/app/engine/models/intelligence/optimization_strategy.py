from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.intelligence.promotion_plan import (
    PromotionPlan,
)


@dataclass(slots=True)
class OptimizationStrategy:
    """
    High-level optimization strategy.

    This is the bridge between the
    Intelligence Engine and the Planner.
    """

    target_role: str

    role_family: str

    categories: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    promotion_plan: PromotionPlan | None = None

    ignored: list[str] = field(
        default_factory=list,
    )

    notes: list[str] = field(
        default_factory=list,
    )
