"""
knowledge_builder.loaders.section_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads section definitions from the Knowledge Database.

Responsibilities
----------------
- Read section JSON files
- Convert dictionaries into Section models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate sections
- Build indexes
- Perform section detection
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    SECTIONS_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Section


class SectionLoader(BaseLoader):
    """
    Loads normalized resume sections.
    """

    def load(self) -> list[Section]:
        """
        Load every section from the configured directory.

        Returns
        -------
        list[Section]
        """
        sections: list[Section] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                sections.append(
                    Section.from_dict(data)
                )

            elif isinstance(data, list):
                sections.extend(
                    Section.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        sections.sort(
            key=lambda section: section.name.casefold()
        )

        return sections

    @classmethod
    def from_default_location(
        cls,
    ) -> "SectionLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(SECTIONS_DIRECTORY)