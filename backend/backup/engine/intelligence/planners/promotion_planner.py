from __future__ import annotations

from app.engine.models.intelligence.promotion_plan import (
    PromotionDecision,
    PromotionPlan,
)
from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


class PromotionPlanner:
    """
    Converts selected technologies into
    promotion decisions.
    """

    # --------------------------------------------------

    def build(
        self,
        technologies: list[SkillPriority],
    ) -> PromotionPlan:

        decisions: list[
            PromotionDecision
        ] = []

        for technology in technologies:

            decisions.append(

                PromotionDecision(

                    technology=technology.technology,

                    section="auto",

                    priority=technology.priority,

                    confidence=1.0,

                    reason=(
                        "Required by target role"
                    ),

                )

            )

        return PromotionPlan(

            decisions=decisions,
        )
