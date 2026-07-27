from __future__ import annotations

from dataclasses import dataclass

from app.engine.intelligence.evidence_engine import (
    TechnologyEvidence,
)
from app.engine.intelligence.priority_engine import (
    PriorityDecision,
)


@dataclass(slots=True, frozen=True)
class PromotionDecision:
    """
    Final decision for one technology.
    """

    technology: str

    category: str

    score: int

    action: str

    reason: str

    evidence: bool


class PromotionEngine:
    """
    Decides whether each technology should be

    • Promote
    • Keep
    • Ignore

    based on evidence and priority.

    This engine NEVER invents experience.
    """

    def build(
        self,
        priorities: list[PriorityDecision],
        evidence: dict[str, TechnologyEvidence],
    ) -> list[PromotionDecision]:

        decisions: list[
            PromotionDecision
        ] = []

        for priority in priorities:

            tech_evidence = evidence.get(
                priority.technology
            )

            if tech_evidence is None:

                decisions.append(

                    PromotionDecision(

                        technology=priority.technology,

                        category=priority.category,

                        score=priority.score,

                        action="ignore",

                        reason="No evidence found.",

                        evidence=False,

                    )

                )

                continue

            if tech_evidence.strong:

                action = "promote"

                reason = (
                    "Strong resume evidence."
                )

            elif (
                tech_evidence.occurrences
                >= 1
            ):

                action = "keep"

                reason = (
                    "Mentioned once."
                )

            else:

                action = "ignore"

                reason = (
                    "Technology not supported."
                )

            decisions.append(

                PromotionDecision(

                    technology=priority.technology,

                    category=priority.category,

                    score=priority.score,

                    action=action,

                    reason=reason,

                    evidence=tech_evidence.strong,

                )

            )

        decisions.sort(

            key=lambda item: item.score,

            reverse=True,

        )

        return decisions




