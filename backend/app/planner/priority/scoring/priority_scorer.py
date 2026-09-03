"""
app.planner.priority.scoring.priority_scorer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scores optimization priorities using prepared
OptimizationKnowledge.
"""

from __future__ import annotations

from app.knowledge.builder.optimization_knowledge import (
    OptimizationSkill,
)


class PriorityScorer:
    """
    Calculates a priority score for an optimization skill.

    The scorer does not access the Knowledge Runtime.
    All required knowledge is supplied by the Planner.
    """

    def score_skill(
        self,
        skill: OptimizationSkill,
    ) -> tuple[float, str]:

        score = 0.0
        reasons: list[str] = []

        # --------------------------------------
        # Role relevance
        # --------------------------------------

        relevance_scores = {
            "required": 50.0,
            "preferred": 30.0,
            "nice_to_have": 15.0,
            "not_listed": 0.0,
        }

        relevance_score = relevance_scores.get(
            skill.role_relevance,
            0.0,
        )

        score += relevance_score

        if skill.role_relevance != "not_listed":
            reasons.append(
                f"Role relevance: {skill.role_relevance}"
            )

        # --------------------------------------
        # User selection
        # --------------------------------------

        if skill.user_selected:
            score += 30.0
            reasons.append(
                "Explicitly selected by the user"
            )

        # --------------------------------------
        # Matched skill
        # --------------------------------------

        if skill.matched:
            score += 10.0
            reasons.append(
                "Already matched in the resume"
            )

        # --------------------------------------
        # Classification
        # --------------------------------------

        if score >= 80:
            level = "critical"
        elif score >= 60:
            level = "high"
        elif score >= 30:
            level = "medium"
        else:
            level = "low"

        reasons.append(
            f"Priority level: {level}"
        )

        return score, "; ".join(reasons)