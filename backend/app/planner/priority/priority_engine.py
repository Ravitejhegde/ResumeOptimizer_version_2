"""
app.planner.priority.priority_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a PriorityPlan from gap analysis and
prepared optimization knowledge.
"""

from __future__ import annotations

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)
from app.knowledge.builder.optimization_knowledge import (
    OptimizationKnowledge,
)
from app.planner.priority.priority_item import (
    PriorityItem,
)
from app.planner.priority.priority_plan import (
    PriorityPlan,
)
from app.planner.priority.scoring.priority_scorer import (
    PriorityScorer,
)


class PriorityEngine:
    """
    Creates a prioritized optimization plan.
    """

    def __init__(self) -> None:
        self._scorer = PriorityScorer()

    def build(
        self,
        gap: GapAnalysisModel,
        job: JobUnderstanding,
        knowledge: OptimizationKnowledge,
    ) -> PriorityPlan:
        """
        Build a prioritized optimization plan.

        Priority is calculated from the prepared
        OptimizationKnowledge rather than directly
        accessing the Knowledge Runtime.
        """

        plan = PriorityPlan()

        # --------------------------------------
        # Optimization Skills
        # --------------------------------------

        for skill in knowledge.optimization_skills:

            score, reason = self._scorer.score_skill(
                skill,
            )

            if score >= 80:
                level = "critical"
            elif score >= 60:
                level = "high"
            elif score >= 30:
                level = "medium"
            else:
                level = "low"

            plan.items.append(
                PriorityItem(
                    id=skill.canonical,
                    type="skill",
                    title=skill.name,
                    description=reason,
                    priority_level=level,
                    priority_score=score,
                    reason=reason,
                    affected_sections=[
                        skill.presentation_category,
                    ],
                    metadata={
                        "canonical": skill.canonical,
                        "taxonomy_category": (
                            skill.taxonomy_category
                        ),
                        "presentation_category": (
                            skill.presentation_category
                        ),
                        "role_relevance": (
                            skill.role_relevance
                        ),
                        "matched": str(
                            skill.matched
                        ),
                        "user_selected": str(
                            skill.user_selected
                        ),
                    },
                )
            )

        plan.sort()

        return plan