"""
knowledge_builder.loaders.category_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads category definitions from JSON files and converts them into
Category domain models.

Source Directory
----------------
knowledge_builder/sources/categories/

Each JSON file may contain:

1. A single category object
2. A list of category objects

The loader performs only parsing and model creation.
Validation belongs to Validators.
Storage belongs to KnowledgeStore.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Category


class CategoryLoader(BaseLoader):
    """
    Loads all knowledge categories.
    """

    def load(self) -> list[Category]:
        """
        Load every category from the source directory.

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
                    f"Unsupported JSON structure in "
                    f"{file_path}"
                )

        categories.sort(
            key=lambda category: category.name.casefold()
        )

        return categories

    @classmethod
    def from_default_location(cls) -> "CategoryLoader":
        """
        Create loader using the standard
        Knowledge Builder directory structure.
        """
        source_directory = (
            Path(__file__).resolve().parent.parent
            / "sources"
            / "categories"
        )

        return cls(source_directory)