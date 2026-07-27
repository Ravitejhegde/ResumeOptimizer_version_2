from __future__ import annotations

from app.engine.intelligence.paragraph_assignment_engine import (
    ParagraphAssignment,
)
from app.engine.intelligence.promotion_engine import (
    PromotionDecision,
)
from app.engine.intelligence.role_classifier import (
    RoleProfile,
)

from app.engine.models.optimization_strategy import (
    OptimizationStrategy,
    TechnologyTarget,
)


class OptimizationStrategyBuilder:
    """
    Builds the shared OptimizationStrategy.

    This is the final output of the
    Intelligence Engine.
    """

    def build(
        self,
        role_profile: RoleProfile,
        promotion_decisions: list[
            PromotionDecision
        ],
        paragraph_assignments: list[
            ParagraphAssignment
        ],
    ) -> OptimizationStrategy:

        strategy = OptimizationStrategy(

            role=role_profile.role,

            role_family=role_profile.role,

        )

        for promotion, assignment in zip(
            promotion_decisions,
            paragraph_assignments,
        ):

            strategy.targets.append(

                TechnologyTarget(

                    technology=promotion.technology,

                    category=promotion.category,

                    score=promotion.score,

                    action=promotion.action,

                    section=assignment.section,

                    paragraph_id=assignment.paragraph_id,

                    reason=promotion.reason,

                )

            )

            if assignment.action != "promote":
                continue

            section = assignment.section.lower()

            if section == "summary":

                strategy.summary_targets.append(
                    assignment.technology
                )

            elif section == "experience":

                strategy.experience_targets.append(
                    assignment.technology
                )

            elif section == "projects":

                strategy.project_targets.append(
                    assignment.technology
                )

            elif section == "skills":

                strategy.skills_targets.append(
                    assignment.technology
                )

        strategy.ignored = [

            target.technology

            for target in strategy.targets

            if target.action == "ignore"

        ]

        return strategy