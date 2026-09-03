"""
app.planner.services.planner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for the Resume Optimization Planner.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)
from app.knowledge.builder.optimization_knowledge import (
    OptimizationKnowledge,
)
from app.planner.blueprint.optimization_blueprint import (
    OptimizationBlueprint,
)
from app.planner.budget.budget_maker import (
    BudgetMaker,
)
from app.planner.decision.decision_engine import (
    DecisionEngine,
)
from app.planner.evidence.evidence_engine import (
    EvidenceEngine,
)
from app.planner.goal.goal_engine import (
    GoalEngine,
)
from app.planner.priority.priority_engine import (
    PriorityEngine,
)
from app.planner.prompt.prompt_planner import (
    PromptPlanner,
)
from app.planner.rewrite.rewrite_planner import (
    RewritePlanner,
)
from app.planner.section.section_planner import (
    SectionPlanner,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class Planner:
    """
    Coordinates all planner engines.
    """

    def __init__(self) -> None:

        self._goal = GoalEngine()

        self._decision = DecisionEngine()

        self._priority = PriorityEngine()

        self._evidence = EvidenceEngine()

        self._section = SectionPlanner()

        self._rewrite = RewritePlanner()

        self._budget = BudgetMaker()

        self._prompt = PromptPlanner()

    def build(
        self,
        document: DocumentModel,
        resume: ResumeUnderstanding,
        job: JobUnderstanding,
        gap: GapAnalysisModel,
        knowledge: OptimizationKnowledge,
    ) -> OptimizationBlueprint:
        """
        Build the complete optimization blueprint.
        """

        blueprint = OptimizationBlueprint()

        # ---------------------------------
        # Knowledge
        # ---------------------------------

        blueprint.knowledge = knowledge

        blueprint.metadata["role_id"] = (
            knowledge.role_id
        )

        blueprint.metadata["role_name"] = (
            knowledge.role_name
        )

        # ---------------------------------
        # Goal
        # ---------------------------------

        blueprint.goal = self._goal.build(
            resume,
            job,
            gap,
        )

        # ---------------------------------
        # Decision
        # ---------------------------------

        blueprint.decision = self._decision.build(
            blueprint.goal,
            gap,
        )

        # ---------------------------------
        # Priority
        # ---------------------------------

        blueprint.priorities = (
            self._priority.build(
                gap,
                job,
                knowledge,
            )
        )

        # ---------------------------------
        # Evidence
        # ---------------------------------

        blueprint.evidence = (
            self._evidence.build(
                document,
                blueprint.priorities,
            )
        )

        # ---------------------------------
        # Section Planning
        # ---------------------------------

        blueprint.section_plan = (
            self._section.build(
                document,
                blueprint.priorities,
                blueprint.evidence,
            )
        )

        # ---------------------------------
        # Rewrite Planning
        # ---------------------------------

        blueprint.rewrite_plan = (
            self._rewrite.build(
                blueprint.decision,
                blueprint.section_plan,
            )
        )

        # ---------------------------------
        # Budget
        # ---------------------------------

        blueprint.budget = (
            self._budget.build(
                blueprint.decision,
                blueprint.priorities,
                blueprint.section_plan,
                blueprint.rewrite_plan,
            )
        )

        # Keep the legacy field synchronized
        # for existing consumers.
        blueprint.token_budget = (
            blueprint.budget.total_tokens
        )

        # ---------------------------------
        # Prompt Planning
        # ---------------------------------

        blueprint.prompt_plan = (
            self._prompt.build(
                blueprint,
            )
        )

        blueprint.prompt_count = (
            blueprint.prompt_plan.prompt_count
        )

        return blueprint