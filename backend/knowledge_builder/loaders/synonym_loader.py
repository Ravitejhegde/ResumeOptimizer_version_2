"""
knowledge_builder.loaders.synonym_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads synonym definitions from the knowledge source directory.

Responsibilities
----------------
- Read JSON files
- Convert dictionaries into Synonym models
- Return strongly typed objects

This loader intentionally does NOT:
- Normalize values
- Validate duplicates
- Resolve technologies
- Store knowledge
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Synonym


class SynonymLoader(BaseLoader):
    """
    Loads normalized synonym definitions.
    """

    def load(self) -> list[Synonym]:
        """
        Load every synonym from the configured source directory.

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
            key=lambda synonym: synonym.canonical.casefold()
        )

        return synonyms

    @classmethod
    def from_default_location(cls) -> "SynonymLoader":
        """
        Create a loader using the default knowledge source directory.
        """
        source_directory = (
            Path(__file__).resolve().parent.parent
            / "sources"
            / "synonyms"
        )

        return cls(source_directory)