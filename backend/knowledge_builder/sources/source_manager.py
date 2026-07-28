from __future__ import annotations

from knowledge_builder.models.category import Category
from knowledge_builder.sources.registry import SourceRegistry


class SourceManager:
    """
    Loads every knowledge source.
    """

    def load_categories(
        self,
    ) -> list[Category]:

        categories: list[Category] = []

        for source in SourceRegistry.all():

            categories.append(
                source.load(),
            )

        return categories