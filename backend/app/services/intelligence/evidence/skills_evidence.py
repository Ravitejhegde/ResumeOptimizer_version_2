from app.services.intelligence.evidence.evidence import Evidence
from app.services.intelligence.const.role_weights import ROLE_WEIGHTS


class SkillsEvidence:

    SKILL_MULTIPLIER = 1.0

    @classmethod
    def build(
        cls,
        technologies,
    ) -> list[Evidence]:

        evidence = []

        if not technologies:
            return evidence

        for technology in technologies:

            # Support both Skill objects and strings
            technology_name = getattr(
                technology,
                "name",
                str(technology),
            )

            key = technology_name.lower().strip()

            for role, weights in ROLE_WEIGHTS.items():

                if key not in weights:
                    continue

                evidence.append(

                    Evidence(

                        role=role,

                        source="skills",

                        confidence=int(
                            weights[key] * cls.SKILL_MULTIPLIER
                        ),

                        technology=technology_name,

                        section="Skills",

                        explanation=f"{technology_name} found in skills",

                    )

                )

        return evidence