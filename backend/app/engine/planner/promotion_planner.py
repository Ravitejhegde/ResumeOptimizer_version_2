from __future__ import annotations

from app.engine.models.promotion_plan import (
    PromotionDecision,
    PromotionPlan,
)


class PromotionPlanner:
    """
    Converts evidence into an optimization plan.

    AI never decides WHAT to promote.

    AI only rewrites.
    """

    @classmethod
    def build(
        cls,
        decisions: list[PromotionDecision],
    ) -> PromotionPlan:

        plan = PromotionPlan()

        for decision in decisions:

            if not decision.evidence_found:

                decision.action = "ignore"

                decision.reason = (
                    "No supporting evidence."
                )

                plan.decisions.append(
                    decision
                )

                continue

            if decision.priority >= 95:

                decision.action = "promote"

                decision.target_section = "summary"

            elif decision.priority >= 85:

                decision.action = "promote"

                decision.target_section = "experience"

            elif decision.priority >= 70:

                decision.action = "promote"

                decision.target_section = "projects"

            else:

                decision.action = "keep"

                decision.target_section = "skills"

            decision.reason = (
                "Priority-based planning."
            )

            plan.decisions.append(
                decision
            )

        return plan




