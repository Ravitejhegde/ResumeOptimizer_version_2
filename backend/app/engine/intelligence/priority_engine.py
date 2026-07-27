from __future__ import annotations

from dataclasses import dataclass

from app.engine.intelligence.technology_ranker import (
    RankedTechnology,
)


@dataclass(slots=True, frozen=True)
class PriorityDecision:
    """
    Final priority assigned to a technology.
    """

    technology: str

    category: str

    score: int

    level: str

    should_promote: bool


class PriorityEngine:
    """
    Calculates the final optimization priority.

    Inputs
    ------
    • Technology importance
    • Resume evidence
    • JD frequency

    Output
    ------
    Final promotion priority.
    """

    HIGH = 90
    MEDIUM = 75
    LOW = 60

    def calculate(
        self,
        ranked: list[RankedTechnology],
        evidence: dict[str, int] | None = None,
        frequency: dict[str, int] | None = None,
    ) -> list[PriorityDecision]:

        evidence = evidence or {}

        frequency = frequency or {}

        decisions: list[
            PriorityDecision
        ] = []

        for technology in ranked:

            score = technology.score

            # -----------------------------
            # Resume already contains it
            # -----------------------------

            score += min(

                evidence.get(
                    technology.technology,
                    0,
                ) * 3,

                15,

            )

            # -----------------------------
            # Frequently mentioned in JD
            # -----------------------------

            score += min(

                frequency.get(
                    technology.technology,
                    0,
                ) * 2,

                10,

            )

            score = min(score, 100)

            if score >= self.HIGH:

                level = "Critical"

            elif score >= self.MEDIUM:

                level = "High"

            elif score >= self.LOW:

                level = "Medium"

            else:

                level = "Low"

            decisions.append(

                PriorityDecision(

                    technology=technology.technology,

                    category=technology.category,

                    score=score,

                    level=level,

                    should_promote=(
                        score >= self.LOW
                    ),

                )

            )

        decisions.sort(

            key=lambda item: item.score,

            reverse=True,

        )

        return decisions




