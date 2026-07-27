from __future__ import annotations

from collections import defaultdict

from app.engine.intelligence.technology_graph import (
    TechnologyGraph,
)


class CategoryClassifier:
    """
    Classifies technologies into categories.

    This class never performs AI.

    It only uses the TechnologyGraph.
    """

    def __init__(self) -> None:

        self._graph = TechnologyGraph()

    def classify(
        self,
        technologies: list[str],
    ) -> dict[str, list[str]]:
        """
        Returns technologies grouped by category.

        Example

        {
            "Backend": [
                "Python",
                "FastAPI"
            ],
            "Frontend": [
                "React"
            ]
        }
        """

        categories: dict[
            str,
            list[str],
        ] = defaultdict(list)

        seen: set[str] = set()

        for technology in technologies:

            node = self._graph.get(
                technology
            )

            if node is None:

                categories[
                    "Other"
                ].append(
                    technology
                )

                continue

            if node.name in seen:
                continue

            seen.add(
                node.name
            )

            categories[
                node.category
            ].append(
                node.name
            )

        return dict(

            sorted(

                categories.items(),

                key=lambda item: item[0],

            )

        )

    def category_of(
        self,
        technology: str,
    ) -> str:

        node = self._graph.get(
            technology
        )

        if node is None:
            return "Other"

        return node.category

    def technologies_in_category(
        self,
        category: str,
    ) -> list[str]:

        result = []

        for node in self._graph.technologies():

            if (
                node.category.lower()
                == category.lower()
            ):

                result.append(
                    node.name
                )

        return sorted(result)

    def available_categories(
        self,
    ) -> list[str]:

        categories = {

            node.category

            for node in self._graph.technologies()

        }

        return sorted(categories)