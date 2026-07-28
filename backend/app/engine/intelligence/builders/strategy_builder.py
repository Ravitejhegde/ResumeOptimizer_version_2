from __future__ import annotations

from app.engine.models.analysis.analysis_result import (
    AnalysisResult,
)
from app.engine.models.intelligence.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.models.intelligence.promotion_plan import (
    PromotionPlan,
)
from app.engine.models.intelligence.role_profile import (
    RoleProfile,
)


class StrategyBuilder:
    """
    Builds the final OptimizationStrategy
    from Intelligence outputs.
    """

    def build(
        self,
        analysis: AnalysisResult,
        role: RoleProfile | None,
        promotion_plan: PromotionPlan,
    ) -> OptimizationStrategy:

        strategy = OptimizationStrategy(

            target_role=(
                role.name
                if role
                else ""
            ),

            role_family=(
                role.category
                if role
                else ""
            ),

            promotion_plan=promotion_plan,
        )

        if analysis.keywords.categories:

            strategy.categories.update(

                analysis.keywords.categories

            )

        return strategy
