"""
knowledge_builder.loaders.relationship_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads relationship definitions from the Knowledge Database.

Responsibilities
----------------
- Read relationship JSON files
- Convert dictionaries into Relationship models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate relationships
- Build indexes
- Build graphs
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    RELATIONSHIPS_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Relationship


class RelationshipLoader(BaseLoader):
    """
    Loads normalized relationships.
    """

    def load(self) -> list[Relationship]:
        """
        Load every relationship from the configured directory.

        Returns
        -------
        list[Relationship]
        """
        relationships: list[Relationship] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                relationships.append(
                    Relationship.from_dict(data)
                )

            elif isinstance(data, list):
                relationships.extend(
                    Relationship.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        relationships.sort(
            key=lambda relationship: (
                relationship.source_id.casefold(),
                relationship.target_id.casefold(),
            )
        )

        return relationships

    @classmethod
    def from_default_location(
        cls,
    ) -> "RelationshipLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(RELATIONSHIPS_DIRECTORY)