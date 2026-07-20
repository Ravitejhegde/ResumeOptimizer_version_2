from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class ProjectsEvidence:

    PROJECT_MULTIPLIER = 1.2

    @classmethod
    def build(
        cls,
        projects,
    ) -> list[Evidence]:

        evidence = []

        if not projects:
            return evidence

        for project in projects:

            for technology in project.technologies:

                key = technology.lower()

                for role, weights in ROLE_WEIGHTS.items():

                    if key not in weights:
                        continue

                    evidence.append(

                        Evidence(

                            role=role,

                            source="projects",

                            confidence=int(
                                weights[key]
                                * cls.PROJECT_MULTIPLIER
                            ),

                            technology=technology,

                            section="Projects",

                            explanation=(
                                f"{technology} used in project"
                            ),

                        )

                    )

        return evidence