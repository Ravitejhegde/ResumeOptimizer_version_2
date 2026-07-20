from app.services.intelligence.evidence.evidence_builder import (
    EvidenceBuilder,
)

from app.services.intelligence.evidence.role_scorer import (
    RoleScorer,
)


class RoleDetector:
    """
    Detects candidate role using evidence aggregation.
    """

    @classmethod
    def detect(
        cls,
        resume,
    ) -> str:

        evidence = EvidenceBuilder.build(
            resume
        )

        scores = RoleScorer.score(
            evidence
        )

        print()
        print("========== ROLE EVIDENCE ==========")

        for item in evidence:

            print(
                f"{item.source:<12}"
                f"{item.role:<25}"
                f"+{item.confidence:<4}"
                f"{item.technology}"
            )

        print()

        print("========== ROLE SCORE ==========")

        ranking = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        for role, score in ranking:

            print(
                f"{role:<25} {score}"
            )

        print()

        if not ranking:

            return "Unknown"

        return ranking[0][0]