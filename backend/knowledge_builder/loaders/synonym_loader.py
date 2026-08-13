"""
knowledge_builder.loaders.synonym_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads synonym definitions from the Knowledge Database.

Responsibilities
----------------
- Read synonym JSON files
- Convert dictionaries into Synonym models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate synonyms
- Build indexes
- Normalize text
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    SYNONYMS_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Synonym


class SynonymLoader(BaseLoader):
    """
    Loads normalized synonyms.
    """

    def load(self) -> list[Synonym]:
        """
        Load every synonym from the configured directory.

        Returns
        -------
        list[Synonym]
        """
        synonyms: list[Synonym] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                synonyms.append(
                    Synonym.from_dict(data)
                )

            elif isinstance(data, list):
                synonyms.extend(
                    Synonym.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        synonyms.sort(
            key=lambda synonym: synonym.id.casefold()
        )

        return synonyms

    @classmethod
    def from_default_location(
        cls,
    ) -> "SynonymLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(SYNONYMS_DIRECTORY)