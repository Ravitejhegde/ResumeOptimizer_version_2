from collections import defaultdict

from app.services.intelligence.evidence.evidence import (
    Evidence,
)


class RoleScorer:
    """
    Aggregates all evidence into role scores.
    """

    @classmethod
    def score(
        cls,
        evidence: list[Evidence],
    ) -> dict[str, int]:

        scores = defaultdict(int)

        for item in evidence:

            scores[item.role] += item.confidence

        return dict(scores)