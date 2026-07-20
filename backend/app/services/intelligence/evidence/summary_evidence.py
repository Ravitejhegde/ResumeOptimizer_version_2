from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SummaryEvidence:

    SUMMARY_MULTIPLIER = 1.0

    @classmethod
    def build(
        cls,
        summary,
    ) -> list[Evidence]:

        evidence = []

        if not summary:
            return evidence

        for technology in summary.technologies:

            key = technology.lower()

            for role, weights in ROLE_WEIGHTS.items():

                if key not in weights:
                    continue

                evidence.append(

                    Evidence(

                        role=role,

                        source="summary",

                        confidence=int(
                            weights[key]
                            * cls.SUMMARY_MULTIPLIER
                        ),

                        technology=technology,

                        section="Summary",

                        explanation=(
                            f"{technology} found in summary"
                        ),

                    )

                )

        return evidence