from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.analysis_result import (
    AnalysisResult,
)
from app.engine.models.document import Document
from app.engine.planner.change_detector import (
    ChangeDecision,
    ChangeDetector,
)
from app.engine.planner.layout_budget_planner import (
    LayoutBudgetPlanner,
    LayoutConstraints,
)
from app.engine.planner.skill_planner import (
    SkillPlan,
    SkillPlanner,
)


@dataclass(slots=True)
class OptimizationPlan:
    """
    Complete optimization plan.

    This is the ONLY object consumed by
    the OptimizationCoordinator.
    """

    document: Document

    paragraph_changes: dict[
        str,
        ChangeDecision,
    ] = field(default_factory=dict)

    rewrite_paragraph_ids: set[str] = field(
        default_factory=set
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
        analysis: AnalysisResult,
        selected_skills: list[str],
    ) -> OptimizationPlan:

        paragraph_changes: dict[
            str,
            ChangeDecision,
        ] = {}

        rewrite_paragraph_ids: set[str] = set()

        layout_constraints: dict[
            str,
            LayoutConstraints,
        ] = {}

        # ----------------------------------------
        # Paragraph Decisions
        # ----------------------------------------

        for paragraph in document.paragraphs:

            decision = ChangeDetector.analyze(
                paragraph
            )

            paragraph_changes[
                paragraph.id
            ] = decision

            if decision.should_rewrite:
                rewrite_paragraph_ids.add(
                    paragraph.id
                )

            if paragraph.layout_budget is not None:

                layout_constraints[
                    paragraph.id
                ] = LayoutBudgetPlanner.build(
                    paragraph.layout_budget
                )

        # ----------------------------------------
        # Skill Plan
        # ----------------------------------------

        skill_plan = self._skill_planner.build(
            resume_skills=analysis.keywords.normalized_skills,
            selected_skills=selected_skills,
        )

        # ----------------------------------------
        # Final Plan
        # ----------------------------------------

        return OptimizationPlan(
            document=document,
            paragraph_changes=paragraph_changes,
            rewrite_paragraph_ids=rewrite_paragraph_ids,
            skill_plan=skill_plan,
            layout_constraints=layout_constraints,
        )