from __future__ import annotations

from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


class TechnologySelector:
    """
    Selects the technologies that should
    be promoted during optimization.
    """

    DEFAULT_LIMIT = 10

    # --------------------------------------------------

    def select(
        self,
        priorities: list[SkillPriority],
        limit: int | None = None,
    ) -> list[SkillPriority]:

        if limit is None:

            limit = self.DEFAULT_LIMIT

        ordered = sorted(

            priorities,

            key=lambda item: item.priority,

            reverse=True,

        )

        selected = ordered[:limit]

        for technology in selected:

            technology.selected = True

        return selected
