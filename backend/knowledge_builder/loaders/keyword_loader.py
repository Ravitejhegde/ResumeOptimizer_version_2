"""
knowledge_builder.loaders.keyword_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads keyword definitions from the Knowledge Database.

Responsibilities
----------------
- Read keyword JSON files
- Convert dictionaries into Keyword models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate keywords
- Build indexes
- Perform keyword matching
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    KEYWORDS_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Keyword


class KeywordLoader(BaseLoader):
    """
    Loads normalized keywords.
    """

    def load(self) -> list[Keyword]:
        """
        Load every keyword from the configured directory.

        Returns
        -------
        list[Keyword]
        """
        keywords: list[Keyword] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                keywords.append(
                    Keyword.from_dict(data)
                )

            elif isinstance(data, list):
                keywords.extend(
                    Keyword.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        keywords.sort(
            key=lambda keyword: keyword.value.casefold()
        )

        return keywords

    @classmethod
    def from_default_location(
        cls,
    ) -> "KeywordLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(KEYWORDS_DIRECTORY)