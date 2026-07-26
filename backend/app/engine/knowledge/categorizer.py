from __future__ import annotations

from collections import defaultdict

from app.engine.knowledge.taxonomy import (
    TechnologyTaxonomy,
)


class SkillCategorizer:
    """
    Organizes technologies into categories
    using the TechnologyTaxonomy.
    """

    def __init__(
        self,
        taxonomy: TechnologyTaxonomy,
    ) -> None:

        self._taxonomy = taxonomy

    def categorize(
        self,
        skills: list[str],
    ) -> dict[str, list[str]]:

        categorized = defaultdict(list)

        for skill in skills:

            category = self._taxonomy.category_of(
                skill
            )

            if category is None:
                category = "unknown"

            categorized[
                category
            ].append(skill)

        return {
            category: sorted(set(values))
            for category, values in categorized.items()
        }