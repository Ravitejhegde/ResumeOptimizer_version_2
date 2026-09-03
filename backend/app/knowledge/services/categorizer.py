from __future__ import annotations

from collections import defaultdict

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class SkillCategorizer:
    """
    Categorizes technologies using the
    Software Engineering Knowledge Domain.
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

    # --------------------------------------------------

    def categorize(
        self,
        skills: list[str],
    ) -> dict[str, list[str]]:

        categorized = defaultdict(list)

        for skill in skills:

            canonical = self._domain.canonical(
                skill,
            )

            category = None

            for category_id, technologies in (
                self._domain.technologies().items()
            ):

                if any(
                    technology["id"] == canonical
                    for technology in technologies
                ):
                    category = category_id
                    break

            if category is None:
                category = "unknown"

            categorized[category].append(skill)

        return {
            category: sorted(set(values))
            for category, values in categorized.items()
        }