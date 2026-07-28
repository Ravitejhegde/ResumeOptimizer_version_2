from __future__ import annotations

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class TechnologyGraph:
    """
    Technology relationship service.

    Uses the Software Engineering Knowledge Domain
    as the single source of truth.
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

    # --------------------------------------------------

    def related_to(
        self,
        technology: str,
    ) -> list[str]:

        return self._domain.related(
            technology,
        )

    # --------------------------------------------------

    def has_relationship(
        self,
        technology_a: str,
        technology_b: str,
    ) -> bool:

        technology_b = self._domain.canonical(
            technology_b,
        )

        return (
            technology_b
            in self._domain.related(
                technology_a,
            )
        )

    # --------------------------------------------------

    def technologies(
        self,
    ) -> list[str]:

        technologies: list[str] = []

        for values in (
            self._domain.technologies().values()
        ):

            technologies.extend(

                technology["id"]

                for technology in values

            )

        return sorted(
            set(technologies),
        )
