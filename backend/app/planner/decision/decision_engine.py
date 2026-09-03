"""
app.planner.decision.decision_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines whether and how aggressively a resume
should be optimized.
"""

from __future__ import annotations

from app.gap_analysis.models.gap_analysis_model import (
    GapAnalysisModel,
)
from app.planner.decision.optimization_decision import (
    OptimizationDecision,
)
from app.planner.goal.optimization_goal import (
    OptimizationGoal,
)


class DecisionEngine:
    """
    Produces an OptimizationDecision.
    """

    def build(
        self,
        goal: OptimizationGoal,
        gap: GapAnalysisModel,
    ) -> OptimizationDecision:

        decision = OptimizationDecision()

        decision.optimization_level = (
            goal.optimization_level
        )

        score = gap.overall_match

        # ------------------------------------
        # Determine optimization strategy
        # ------------------------------------

        if score >= 0.90:

            decision.should_optimize = True
            decision.strategy = (
                "ATS polishing"
            )
            decision.reason = (
                "Resume already closely matches the job."
            )

        elif score >= 0.70:

            decision.should_optimize = True
            decision.strategy = (
                "Moderate optimization"
            )
            decision.reason = (
                "Resume requires targeted improvements."
            )

        elif score >= 0.40:

            decision.should_optimize = True
            decision.strategy = (
                "Major optimization"
            )
            decision.reason = (
                "Resume has significant gaps."
            )

        else:

            decision.should_optimize = True
            decision.strategy = (
                "Career transition"
            )
            decision.reason = (
                "Large role mismatch detected."
            )

            decision.warnings.append(
                "Avoid introducing unsupported experience."
            )

        return decision