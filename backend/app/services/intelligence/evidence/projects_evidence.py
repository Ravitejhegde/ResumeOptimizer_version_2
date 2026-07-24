from app.services.intelligence.evidence.evidence import (
    Evidence,
)

from app.services.intelligence.const.role_weights import (
    ROLE_WEIGHTS,
)


class ProjectsEvidence:
    """
    Builds evidence from technologies found
    in projects.
    """

    PROJECT_MULTIPLIER = 1.2

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

                        source="projects",

                        confidence=int(
                            weights[key]
                            * cls.PROJECT_MULTIPLIER
                        ),

                        technology=technology,

                        section="Projects",

                        explanation=(
                            f"{technology} found in projects"
                        ),

                    )

                )

        return evidence