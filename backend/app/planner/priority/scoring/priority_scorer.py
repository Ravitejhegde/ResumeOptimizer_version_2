"""
app.planner.priority.scoring.priority_scorer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scores optimization priorities.
"""

from __future__ import annotations

from app.knowledge.provider import (
    get_knowledge,
)


class PriorityScorer:
    """
    Calculates a priority score for an optimization item.
    """

    def __init__(self) -> None:
        self._runtime = get_knowledge()

    def score_skill(
        self,
        skill_id: str,
        target_role: str,
    ) -> tuple[int, str]:

        score = 0
        reasons: list[str] = []

        skill = self._runtime.skills.find_by_id(
            skill_id
        )

        if skill is not None:

            importance = skill.get(
                "importance",
                0,
            )

            score += importance * 10

            reasons.append(
                f"Knowledge importance {importance}"
            )

        role = self._runtime.roles.find_by_id(
            target_role
        )

        if (
            role
            and skill_id
            in role.get(
                "required_skill_ids",
                [],
            )
        ):
            score += 50

            reasons.append(
                "Required by target role"
            )

        return (
            score,
            "; ".join(reasons),
        )