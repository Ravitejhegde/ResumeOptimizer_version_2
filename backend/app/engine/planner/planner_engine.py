from __future__ import annotations

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.intelligence.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)
from app.engine.planner.allocators.budget_allocator import (
    BudgetAllocator,
)
from app.engine.planner.builders.optimization_plan_builder import (
    OptimizationPlanBuilder,
)
from app.engine.planner.builders.rewrite_plan_builder import (
    RewritePlanBuilder,
)
from app.engine.planner.builders.section_plan_builder import (
    SectionPlanBuilder,
)
from app.engine.planner.validators.plan_validator import (
    PlanValidator,
)


class PlannerEngine:
    """
    Builds the complete execution plan.

    Intelligence
        ↓
    Planner
        ↓
    Optimizer
    """

    def __init__(
        self,
    ) -> None:

        self._optimization = (
            OptimizationPlanBuilder()
        )

        self._sections = (
            SectionPlanBuilder()
        )

        self._allocator = (
            BudgetAllocator()
        )

        self._rewrites = (
            RewritePlanBuilder()
        )

        self._validator = (
            PlanValidator()
        )

    # --------------------------------------------------

    def build(
        self,
        strategy: OptimizationStrategy,
        document: Document,
    ) -> OptimizationPlan:

        plan = self._optimization.build(
            strategy,
        )

        plan = self._sections.build(
            plan,
        )

        plan = self._allocator.allocate(
            plan,
            document,
        )

        plan = self._rewrites.build(
            plan,
        )

        plan = self._validator.validate(
            plan,
        )

        return plan
