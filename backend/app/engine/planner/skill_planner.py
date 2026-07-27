from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)


@dataclass(slots=True)
class SkillPlan:
    """
    Simple skill planning.

    Intelligence is handled by
    IntelligenceEngine.
    """

    existing_skills: list[str] = field(
        default_factory=list
    )

    selected_skills: list[str] = field(
        default_factory=list
    )

    missing_skills: list[str] = field(
        default_factory=list
    )

    categorized_skills: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict
    )


class SkillPlanner:
    """
    Builds the basic skill plan.

    Role detection, prioritization,
    categorization and promotion are now
    handled by IntelligenceEngine.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._knowledge = knowledge

    def build(
        self,
        resume_skills: list[str],
        selected_skills: list[str],
    ) -> SkillPlan:

        existing = sorted(

            self._knowledge.normalizer.normalize_many(
                resume_skills
            )

        )

        selected = sorted(

            self._knowledge.normalizer.normalize_many(
                selected_skills
            )

        )

        missing = sorted(

            skill

            for skill in selected

            if skill not in existing

        )

        categorized = (

            self._knowledge.categorizer.categorize(

                sorted(
                    set(existing).union(
                        selected
                    )
                )

            )

        )

        return SkillPlan(

            existing_skills=existing,

            selected_skills=selected,

            missing_skills=missing,

            categorized_skills=categorized,

        )