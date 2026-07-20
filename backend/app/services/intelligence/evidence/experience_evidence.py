from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class ExperienceEvidence:

    EXPERIENCE_MULTIPLIER = 1.5

    @classmethod
    def build(
        cls,
        experiences,
    ) -> list[Evidence]:

        evidence = []

        if not experiences:
            return evidence

        for experience in experiences:

            for technology in experience.technologies:

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
                                f"{technology} used in work experience"
                            ),

                        )

                    )

        return evidence