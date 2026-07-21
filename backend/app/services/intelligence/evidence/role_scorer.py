from collections import defaultdict

from app.services.intelligence.evidence.evidence import (
    Evidence,
)


class RoleScorer:

    SOURCE_WEIGHTS = {

        "title": 3.0,

        "experience": 2.5,

        "projects": 2.0,

        "summary": 1.5,

        "skills": 1.0,

    }

    @classmethod
    def score(
        cls,
        evidence: list[Evidence],
    ) -> dict[str, int]:

        scores = defaultdict(float)

        for item in evidence:

            multiplier = cls.SOURCE_WEIGHTS.get(
                item.source.lower(),
                1.0,
            )

            scores[item.role] += (
                item.confidence * multiplier
            )

        return {

            role: round(score)

            for role, score in scores.items()

        }