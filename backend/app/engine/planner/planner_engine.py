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


from app.engine.planner.builders.optimization_plan_builder import (
    OptimizationPlanBuilder,
)

from app.engine.planner.builders.section_plan_builder import (
    SectionPlanBuilder,
)

from app.engine.planner.builders.rewrite_plan_builder import (
    RewritePlanBuilder,
)

from app.engine.planner.allocators.budget_allocator import (
    BudgetAllocator,
)

from app.engine.planner.validators.plan_validator import (
    PlanValidator,
)



class PlannerEngine:
    """
    Builds complete optimization execution plan.


    Pipeline:

        Optimization Strategy
                |
                v
        OptimizationPlanBuilder
                |
                v
        SectionPlanBuilder
                |
                v
        BudgetAllocator
                |
                v
        RewritePlanBuilder
                |
                v
        PlanValidator
                |
                v
        OptimizationPlan
    """


    def __init__(
        self,
    ) -> None:


        self._optimization_builder = (
            OptimizationPlanBuilder()
        )


        self._section_builder = (
            SectionPlanBuilder()
        )


        self._budget_allocator = (
            BudgetAllocator()
        )


        self._rewrite_builder = (
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


        print(
            "\n========== PLANNER =========="
        )


        # ----------------------------------
        # Step 1
        # Create optimization plan
        # ----------------------------------

        plan = (
            self._optimization_builder.build(
                strategy
            )
        )


        print(
            "After OptimizationPlanBuilder:"
        )

        print(
            f"Sections: {len(plan.sections)}"
        )

        print(
            f"Rewrites: {len(plan.rewrites)}"
        )



        # ----------------------------------
        # Step 2
        # Attach document paragraphs
        # ----------------------------------

        section_plans = (
            self._section_builder.build(
                promotion_plan=(
                    strategy.promotion_plan
                ),
                document=document,
            )
        )


        plan.sections = section_plans



        print(
            "\nAfter SectionPlanBuilder:"
        )

        print(
            f"Sections: {len(plan.sections)}"
        )

        print(
            f"Rewrites: {len(plan.rewrites)}"
        )



        # ----------------------------------
        # Step 3
        # Allocate layout budget
        # ----------------------------------

        plan = (
            self._budget_allocator.allocate(
                plan,
                document,
            )
        )


        print(
            "\nAfter BudgetAllocator:"
        )

        print(
            f"Sections: {len(plan.sections)}"
        )

        print(
            f"Rewrites: {len(plan.rewrites)}"
        )



        # ----------------------------------
        # Step 4
        # Create rewrite instructions
        # ----------------------------------

        plan = (
            self._rewrite_builder.build(
                plan
            )
        )


        print(
            "\nAfter RewritePlanBuilder:"
        )

        print(
            f"Sections: {len(plan.sections)}"
        )

        print(
            f"Rewrites: {len(plan.rewrites)}"
        )



        # ----------------------------------
        # Step 5
        # Validate final plan
        # ----------------------------------

        plan = (
            self._validator.validate(
                plan
            )
        )


        print(
            "\nAfter PlanValidator:"
        )

        print(
            f"Sections: {len(plan.sections)}"
        )

        print(
            f"Rewrites: {len(plan.rewrites)}"
        )


        print(
            "=============================\n"
        )


        return plan