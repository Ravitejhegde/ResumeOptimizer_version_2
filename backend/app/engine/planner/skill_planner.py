from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


@dataclass(slots=True)
class SkillPlan:
    """
    Execution-ready skill plan.

    IntelligenceEngine decides WHAT should
    be promoted.

    SkillPlanner prepares the data required
    by the optimizer.
    """

    existing_skills: list[str] = field(
        default_factory=list,
    )

    selected_skills: list[str] = field(
        default_factory=list,
    )

    missing_skills: list[str] = field(
        default_factory=list,
    )

    categorized_skills: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )


class SkillPlanner:
    """
    Converts analyzed skills into an
    execution-ready plan.

    This class performs lightweight
    preparation only.

    It does NOT:
    - detect roles
    - rank skills
    - prioritize skills
    - call AI
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

    def build(
        self,
        resume_skills: list[str],
        selected_skills: list[str],
    ) -> SkillPlan:
        """
        Build a skill plan for execution.
        """

        existing = self._knowledge.normalize_many(
            resume_skills,
        )

        selected = self._knowledge.normalize_many(
            selected_skills,
        )

        missing = sorted(

            skill

            for skill in selected

            if skill not in existing

        )

        categorized = self._knowledge.categorize(

            sorted(

                set(existing).union(
                    selected,
                )

            )

        )

        return SkillPlan(

            existing_skills=existing,

            selected_skills=selected,

            missing_skills=missing,

            categorized_skills=categorized,

        )