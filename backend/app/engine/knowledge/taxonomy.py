from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TechnologyTaxonomy:
    """
    Central technology taxonomy.

    Stores all supported technologies grouped by category.
    """

    technologies: dict[str, set[str]] = field(
        default_factory=dict
    )

    def register(
        self,
        category: str,
        *values: str,
    ) -> None:

        category = category.lower()

        if category not in self.technologies:
            self.technologies[category] = set()

        for value in values:
            self.technologies[category].add(
                value.lower()
            )

    def contains(
        self,
        technology: str,
    ) -> bool:

        technology = technology.lower()

        return any(
            technology in values
            for values in self.technologies.values()
        )

    def category_of(
        self,
        technology: str,
    ) -> str | None:

        technology = technology.lower()

        for category, values in self.technologies.items():

            if technology in values:
                return category

        return None