from app.services.intelligence.evidence.evidence_builder import (
    EvidenceBuilder,
)

from app.services.intelligence.evidence.role_scorer import (
    RoleScorer,
)

from app.services.intelligence.evidence.role_ranker import (
    RoleRanker,
)


class RoleDetector:
    """
    Detects the candidate role using
    evidence aggregation and role ranking.
    """

    @classmethod
    def detect(
        cls,
        resume,
    ) -> str:

        # -----------------------------------------
        # Build Evidence
        # -----------------------------------------

        evidence = EvidenceBuilder.build(
            resume
        )

        # -----------------------------------------
        # Score Roles
        # -----------------------------------------

        scores = RoleScorer.score(
            evidence
        )

        # -----------------------------------------
        # Print Evidence
        # -----------------------------------------

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

        # -----------------------------------------
        # Rank Roles
        # -----------------------------------------

        ranking = RoleRanker.rank(
            scores
        )

        if not ranking:

            print("No role detected.")
            return "Unknown"

        # -----------------------------------------
        # Print Ranking
        # -----------------------------------------

        print("========== ROLE RANKING ==========")

        for item in ranking:

            print(

                f"{item['role']:<25}"

                f"{item['score']:>5}"

                f"   ({item['confidence']}%)"

            )

        print()

        # -----------------------------------------
        # Best Match
        # -----------------------------------------

        top = ranking[0]

        print(
            f"Predicted Role : {top['role']}"
        )

        print(
            f"Confidence     : {top['confidence']}%"
        )

        print()

        return top["role"]