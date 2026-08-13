"""
knowledge_builder.loaders.role_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads role definitions from the Knowledge Database.

Responsibilities
----------------
- Read role JSON files
- Convert dictionaries into Role models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate roles
- Build indexes
- Build relationships
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    ROLES_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Role


class RoleLoader(BaseLoader):
    """
    Loads normalized job roles.
    """

    def load(self) -> list[Role]:
        """
        Load every role from the configured directory.

        Returns
        -------
        list[Role]
        """
        roles: list[Role] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                roles.append(
                    Role.from_dict(data)
                )

            elif isinstance(data, list):
                roles.extend(
                    Role.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        roles.sort(
            key=lambda role: role.name.casefold()
        )

        return roles

    @classmethod
    def from_default_location(
        cls,
    ) -> "RoleLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(ROLES_DIRECTORY)