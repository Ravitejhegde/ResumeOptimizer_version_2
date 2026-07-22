from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SkillsEvidence:
    """
    Builds evidence from ResumeKnowledge technologies.
    """

    @classmethod
    def build(
        cls,
        technologies: list[str],
    ) -> list[Evidence]:

        evidence = []

        for technology in technologies:

            key = technology.lower().strip()

            for role, weights in ROLE_WEIGHTS.items():

                if key not in weights:
                    continue

                confidence = weights[key]

                evidence.append(

                    Evidence(

                        role=role,

                        source="skills",

                        confidence=confidence,

                        technology=technology,

                        section="Skills",

                        explanation=(
                            f"{technology} supports {role}"
                        ),

                    )

                )

        return evidence