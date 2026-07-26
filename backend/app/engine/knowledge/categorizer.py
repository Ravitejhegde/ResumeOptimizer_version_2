from __future__ import annotations

from collections import defaultdict


class SkillCategorizer:
    """
    Organizes technologies into logical categories.

    The categorizer NEVER guesses categories.

    It uses the TechnologyTaxonomy as the
    single source of truth.
    """

    def __init__(
        self,
        taxonomy,
    ) -> None:

        self._taxonomy = taxonomy

    def categorize(
        self,
        skills: list[str],
    ) -> dict[str, list[str]]:

        categorized = defaultdict(list)

        unknown = []

        for skill in skills:

            technology = self._taxonomy.get(skill)

            if technology is None:

                unknown.append(skill)

                continue

            categorized[
                technology.category
            ].append(
                technology.name
            )

        if unknown:

            categorized[
                "Unknown"
            ] = sorted(
                unknown
            )

        result = {}

        for category in sorted(categorized):

            result[
                category
            ] = sorted(
                set(
                    categorized[
                        category
                    ]
                )
            )

        return result