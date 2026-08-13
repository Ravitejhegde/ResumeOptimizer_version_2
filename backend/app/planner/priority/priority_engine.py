"""
app.planner.priority.priority_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a PriorityPlan from the gap analysis.
"""

from __future__ import annotations

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
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
    ) -> PriorityPlan:
        """
        Build a prioritized optimization plan from the gap analysis.
        """

        plan = PriorityPlan()

        target_role = (
            job.target_role.casefold()
            .replace(" ", "_")
        )

        # --------------------------------------
        # Missing Skills
        # --------------------------------------

        for skill in gap.missing_skills:

            skill_id = (
                skill.casefold()
                .replace(" ", "_")
            )

            score, reason = self._scorer.score_skill(
                skill_id,
                target_role,
            )

            if score >= 90:
                level = "critical"
            elif score >= 70:
                level = "high"
            elif score >= 40:
                level = "medium"
            else:
                level = "low"

            plan.items.append(
                PriorityItem(
                    id=skill_id,
                    type="skill",
                    title=skill,
                    description=reason,
                    priority_level=level,
                    priority_score=score,
                    reason=reason,
                    affected_sections=[
                        "Experience",
                    ],
                )
            )

        # --------------------------------------
        # Missing Technologies
        # --------------------------------------

        for technology in gap.missing_technologies:

            technology_id = (
                technology.casefold()
                .replace(" ", "_")
            )

            score = 80.0

            reason = (
                "Required technology is missing."
            )

            plan.items.append(
                PriorityItem(
                    id=technology_id,
                    type="technology",
                    title=technology,
                    description=reason,
                    priority_level="high",
                    priority_score=score,
                    reason=reason,
                    affected_sections=[
                        "Experience",
                    ],
                )
            )

        plan.sort()

        return plan