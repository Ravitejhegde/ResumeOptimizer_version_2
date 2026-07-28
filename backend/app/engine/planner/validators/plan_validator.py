from __future__ import annotations

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)


class PlanValidator:
    """
    Validates the OptimizationPlan before
    it reaches the Optimizer.
    """

    # --------------------------------------------------

    def validate(
        self,
        plan: OptimizationPlan,
    ) -> OptimizationPlan:

        warnings: list[str] = []

        if not plan.sections:

            warnings.append(
                "No sections selected for optimization."
            )

        if not plan.rewrites:

            warnings.append(
                "No rewrite operations generated."
            )

        plan.warnings.extend(
            warnings,
        )

        return plan
