from __future__ import annotations

from app.engine.models.intelligence.skill_gap import (
    SkillGap,
)
from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


class PriorityScorer:
    """
    Assigns optimization priorities to
    missing technologies.
    """

    def score(
        self,
        skill_gap: SkillGap,
    ) -> list[SkillPriority]:

        priorities: list[SkillPriority] = []

        priority = 100

        for skill in skill_gap.missing:

            priorities.append(

                SkillPriority(

                    technology=skill.technology,

                    category=skill.category,

                    priority=priority,

                    matched=False,

                    selected=False,

                )

            )

            priority = max(
                priority - 5,
                10,
            )

        return priorities
