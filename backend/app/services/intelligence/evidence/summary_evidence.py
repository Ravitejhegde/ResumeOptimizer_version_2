from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SummaryEvidence:
    """
    Builds evidence from the resume summary.
    """

    SUMMARY_MULTIPLIER = 1.0

    @classmethod
    def build(
        cls,
        summary,
        skills,
    ) -> list[Evidence]:

        evidence = []

        if summary is None:
            return evidence

        summary_text = getattr(
            summary,
            "text",
            "",
        )

        if not summary_text:
            return evidence

        summary_lower = summary_text.lower()

        for skill in skills:

            skill_name = getattr(
                skill,
                "name",
                str(skill),
            )

            if skill_name.lower() not in summary_lower:
                continue

            key = skill_name.lower()

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

                        technology=skill_name,

                        section="Summary",

                        explanation=f"{skill_name} found in summary",

                    )

                )

        return evidence