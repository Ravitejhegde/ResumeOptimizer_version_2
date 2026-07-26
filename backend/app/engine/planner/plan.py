from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document import Document
from app.engine.planner.change_detector import (
    ChangeDecision,
    ChangeDetector,
)
from app.engine.planner.skill_planner import (
    SkillPlan,
    SkillPlanner,
)
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.planner.layout_budget_planner import (
    LayoutBudgetPlanner,
    LayoutConstraints,
)


@dataclass(slots=True)
class OptimizationPlan:
    """
    Master optimization plan.

    This is the ONLY object passed to the
    Optimizer module.
    """

    document: Document

    paragraph_changes: list[ChangeDecision] = field(
        default_factory=list
    )

    skill_plan: SkillPlan | None = None

    layout_constraints: dict[
        str,
        LayoutConstraints,
    ] = field(default_factory=dict)


class PlanBuilder:
    """
    Builds the complete optimization plan.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._skill_planner = SkillPlanner(
            knowledge
        )

    def build(
        self,
        document: Document,
        resume_skills: list[str],
        selected_skills: list[str],
    ) -> OptimizationPlan:

        # ----------------------------------------
        # Paragraph decisions
        # ----------------------------------------

        paragraph_changes = [
            ChangeDetector.analyze(paragraph)
            for paragraph in document.paragraphs
        ]

        # ----------------------------------------
        # Skill plan
        # ----------------------------------------

        skill_plan = self._skill_planner.build(
            resume_skills=resume_skills,
            selected_skills=selected_skills,
        )

        # ----------------------------------------
        # Layout constraints
        # ----------------------------------------

        layout_constraints: dict[
            str,
            LayoutConstraints,
        ] = {}

        for paragraph in document.paragraphs:

            if paragraph.layout_budget is None:
                continue

            layout_constraints[
                paragraph.id
            ] = LayoutBudgetPlanner.build(
                paragraph.layout_budget
            )

        # ----------------------------------------
        # Build optimization plan
        # ----------------------------------------

        return OptimizationPlan(
            document=document,
            paragraph_changes=paragraph_changes,
            skill_plan=skill_plan,
            layout_constraints=layout_constraints,
        )