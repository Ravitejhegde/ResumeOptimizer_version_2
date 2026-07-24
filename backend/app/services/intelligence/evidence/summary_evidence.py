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
    """

    SUMMARY_MULTIPLIER = 1.0

    @classmethod
    def build(
        cls,
        summary,
        technologies: list[str],
    ) -> list[Evidence]:

        evidence = []

        if not summary:
            return evidence

        summary_text = getattr(
            summary,
            "text",
            "",
        )

        if not summary_text:
            return evidence

        summary_lower = summary_text.lower()

        for technology in technologies:

            technology_name = getattr(
            technology,
            "name",
            str(technology),
        )

            if technology_name.lower() not in summary_lower:
                continue

            key = technology_name.lower()

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

                        technology=technology_name,


                        section="Summary",

                        explanation=f"{technology_name} found in summary",


                    )

                )

        return evidence