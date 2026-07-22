from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class ExperienceEvidence:
    """
    Builds evidence from technologies found
    in work experience.
    """

    EXPERIENCE_MULTIPLIER = 1.5

    @classmethod
    def build(
        cls,
        technologies: list[str],
    ) -> list[Evidence]:

        evidence = []

        for technology in technologies:

            key = technology.lower()

            for role, weights in ROLE_WEIGHTS.items():

                if key not in weights:
                    continue

                evidence.append(

                    Evidence(

                        role=role,

                        source="experience",

                        confidence=int(
                            weights[key]
                            * cls.EXPERIENCE_MULTIPLIER
                        ),

                        technology=technology,

                        section="Experience",

                        explanation=(
                            f"{technology} found in work experience"
                        ),

                    )

                )

        return evidence