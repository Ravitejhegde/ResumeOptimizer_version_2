from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)


@dataclass(slots=True, frozen=True)
class SkillPlan:
    """
    Planning result for the Skills section.

    The planner never modifies the resume.
    It only decides WHAT should happen.
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
    Creates the optimization plan for the
    Skills section.

    Responsibilities
    ----------------
    • Normalize skills
    • Remove duplicates
    • Detect missing skills
    • Categorize technologies

    Never edits the document.
    Never calls AI.
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

        existing = (
            self._knowledge.normalizer.normalize_many(
                resume_skills
            )
        )

        selected = (
            self._knowledge.normalizer.normalize_many(
                selected_skills
            )
        )

        existing_set = set(existing)

        missing = sorted(

            skill

            for skill in selected

            if skill not in existing_set

        )

        merged = sorted(

            existing_set.union(
                selected
            )

        )

        categorized = (
            self._knowledge.categorizer.categorize(
                merged
            )
        )

        return SkillPlan(

            existing_skills=existing,

            selected_skills=selected,

            missing_skills=missing,

            categorized_skills=categorized,

        )