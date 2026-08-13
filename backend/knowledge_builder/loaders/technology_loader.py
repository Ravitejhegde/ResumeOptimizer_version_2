"""
knowledge_builder.loaders.technology_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads technology definitions from the Knowledge Database.

Responsibilities
----------------
- Read technology JSON files
- Convert dictionaries into Technology models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate technologies
- Build indexes
- Build relationships
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    TECHNOLOGIES_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Technology


class TechnologyLoader(BaseLoader):
    """
    Loads normalized technologies.
    """

    def load(self) -> list[Technology]:
        """
        Load every technology from the configured directory.

        Returns
        -------
        list[Technology]
        """
        technologies: list[Technology] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                technologies.append(
                    Technology.from_dict(data)
                )

            elif isinstance(data, list):
                technologies.extend(
                    Technology.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        technologies.sort(
            key=lambda technology: technology.name.casefold()
        )

        return technologies

    @classmethod
    def from_default_location(
        cls,
    ) -> "TechnologyLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(TECHNOLOGIES_DIRECTORY)