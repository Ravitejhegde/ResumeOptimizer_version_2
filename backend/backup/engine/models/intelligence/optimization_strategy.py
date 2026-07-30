from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.intelligence.promotion_plan import (
    PromotionPlan,
)


@dataclass(slots=True)
class OptimizationStrategy:
    """
    High-level optimization strategy.

    Bridge between:

        Intelligence Engine
              ↓
            Planner

    Contains decisions about what should
    improve in the resume.

    It does NOT perform rewriting.
    """

    # --------------------------------------------------
    # Target Role
    # --------------------------------------------------

    target_role: str

    role_family: str

    confidence: float = 0.0

    knowledge_role_id: str | None = None

    # --------------------------------------------------
    # Skill Direction
    # --------------------------------------------------

    categories: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Promotion Decisions
    # --------------------------------------------------

    promotion_plan: PromotionPlan | None = None

    # --------------------------------------------------
    # Optimization Goals
    # --------------------------------------------------

    goals: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Excluded Items
    # --------------------------------------------------

    ignored: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    notes: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_promotion_plan(
        self,
    ) -> bool:

        return (
            self.promotion_plan is not None
            and bool(
                self.promotion_plan.decisions
            )
        )

    def is_confident(
        self,
        threshold: float = 0.7,
    ) -> bool:

        return self.confidence >= threshold