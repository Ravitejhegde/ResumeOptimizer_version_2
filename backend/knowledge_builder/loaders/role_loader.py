"""
knowledge_builder.loaders.role_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads normalized job roles from the knowledge source directory.

Responsibilities
----------------
- Read JSON files
- Convert dictionaries into Role models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate roles
- Match technologies
- Match skills
- Build relationships
- Store data
"""

from __future__ import annotations

from pathlib import Path

from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Role


class RoleLoader(BaseLoader):
    """
    Loads normalized job roles.
    """

    def load(self) -> list[Role]:
        """
        Load every role from the configured source directory.

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
    def from_default_location(cls) -> "RoleLoader":
        """
        Create a loader using the default source directory.
        """
        source_directory = (
            Path(__file__).resolve().parent.parent
            / "sources"
            / "roles"
        )

        return cls(source_directory)