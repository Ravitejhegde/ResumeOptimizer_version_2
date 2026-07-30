"""
knowledge_builder.builders.category_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds fast lookup indexes for Category objects.

Indexes produced
----------------
- By ID
- By normalized name
- By normalized alias

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Category


@dataclass(slots=True)
class CategoryIndex:
    """
    Fast lookup structure for categories.
    """

    by_id: dict[str, Category] = field(default_factory=dict)
    by_name: dict[str, Category] = field(default_factory=dict)
    by_alias: dict[str, Category] = field(default_factory=dict)

    @property
    def size(self) -> int:
        """
        Number of indexed categories.
        """
        return len(self.by_id)

    def get_by_id(self, category_id: str) -> Category | None:
        return self.by_id.get(category_id)

    def get_by_name(self, name: str) -> Category | None:
        return self.by_name.get(name.casefold())

    def get_by_alias(self, alias: str) -> Category | None:
        return self.by_alias.get(alias.casefold())

    def find(self, value: str) -> Category | None:
        """
        Find a category using ID, name, or alias.
        """
        return (
            self.by_id.get(value)
            or self.by_name.get(value.casefold())
            or self.by_alias.get(value.casefold())
        )


class CategoryIndexBuilder(BaseBuilder[CategoryIndex]):
    """
    Builds optimized category lookup indexes.
    """

    def build(self) -> CategoryIndex:
        index = CategoryIndex()

        for category in self.store.categories.values():

            if category.id in index.by_id:
                raise ValueError(
                    f"Duplicate category id '{category.id}'."
                )

            index.by_id[category.id] = category

            normalized_name = category.name.casefold()

            if normalized_name in index.by_name:
                raise ValueError(
                    f"Duplicate category name '{category.name}'."
                )

            index.by_name[normalized_name] = category

            for alias in category.aliases:

                normalized_alias = alias.casefold()

                if normalized_alias in index.by_alias:
                    raise ValueError(
                        f"Duplicate category alias '{alias}'."
                    )

                index.by_alias[normalized_alias] = category

        return index