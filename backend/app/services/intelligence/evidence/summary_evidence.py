from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SummaryEvidence:
    """
    Builds evidence from technologies found in the
    resume summary.

    In the new architecture the summary is plain text,
    while the extracted technologies are stored in
    ResumeKnowledge. Therefore this builder receives
    both values.
    """

    SUMMARY_MULTIPLIER = 1.0

    @classmethod
    def build(
        cls,
        summary: str,
        technologies: list[str],
    ) -> list[Evidence]:

        evidence = []

        if not summary:
            return evidence

        summary_lower = summary.lower()

        for technology in technologies:

            if technology.lower() not in summary_lower:
                continue

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

                        explanation=f"{technology} found in summary",

                    )

                )

        return evidence