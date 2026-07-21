from collections import defaultdict

from app.services.intelligence.evidence.evidence import (
    Evidence,
)


class EvidenceOptimizer:
    """
    Removes duplicate evidence and
    keeps the strongest evidence for each
    (role, technology, source) combination.
    """

    @classmethod
    def optimize(
        cls,
        evidence: list[Evidence],
    ) -> list[Evidence]:

        best: dict[
            tuple[str, str, str],
            Evidence,
        ] = {}

        for item in evidence:

            key = (

                item.role,

                item.source,

                (item.technology or "").lower(),

            )

            if (
                key not in best
                or item.confidence
                > best[key].confidence
            ):

                best[key] = item

        return list(best.values())