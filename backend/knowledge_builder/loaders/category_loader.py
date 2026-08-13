"""
knowledge_builder.loaders.category_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads category definitions from the Knowledge Database.

Responsibilities
----------------
- Read category JSON files
- Convert dictionaries into Category models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate categories
- Build indexes
- Build relationships
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    CATEGORIES_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Category


class CategoryLoader(BaseLoader):
    """
    Loads normalized categories.
    """

    def load(self) -> list[Category]:
        """
        Load every category from the configured directory.

        Returns
        -------
        list[Category]
        """
        categories: list[Category] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                categories.append(
                    Category.from_dict(data)
                )

            elif isinstance(data, list):
                categories.extend(
                    Category.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        categories.sort(
            key=lambda category: category.name.casefold()
        )

        return categories

    @classmethod
    def from_default_location(
        cls,
    ) -> "CategoryLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(CATEGORIES_DIRECTORY)