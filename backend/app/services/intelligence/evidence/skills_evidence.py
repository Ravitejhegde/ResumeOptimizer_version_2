from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SkillsEvidence:
    """
    Builds evidence from detected resume skills.
    """

    @classmethod
    def build(
        cls,
        skills,
    ) -> list[Evidence]:

        evidence = []

        for skill in skills:

            technology = (
                skill.name.lower().strip()
            )

            for role, weights in ROLE_WEIGHTS.items():

                if technology not in weights:
                    continue

                weight = weights[
                    technology
                ]

                evidence.append(

                    Evidence(

                        role=role,

                        source="skills",

                        confidence=weight,

                        technology=skill.name,

                        section=skill.section,

                        explanation=(
                            f"{skill.name} "
                            f"supports {role}"
                        ),

                    )

                )

        return evidence