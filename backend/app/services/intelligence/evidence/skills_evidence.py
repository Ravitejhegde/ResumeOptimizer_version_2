from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class SkillsEvidence:
    """
    Builds evidence from detected skills.
    """

    SKILL_MULTIPLIER = 1.2

    @classmethod
    def build(
        cls,
        skills,
    ) -> list[Evidence]:

        evidence = []

        for skill in skills:

            skill_name = getattr(
                skill,
                "name",
                str(skill),
            )

            key = skill_name.lower().strip()

            for role, weights in ROLE_WEIGHTS.items():

                if key not in weights:
                    continue

                evidence.append(

                    Evidence(

                        role=role,

                        source="skills",

                        confidence=int(
                            weights[key]
                            * cls.SKILL_MULTIPLIER
                        ),

                        technology=skill_name,

                        section="Skills",

                        explanation=f"{skill_name} found in skills",

                    )

                )

        return evidence