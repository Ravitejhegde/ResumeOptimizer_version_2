"""
knowledge_builder.loaders.skill_loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Loads skill definitions from the Knowledge Database.

Responsibilities
----------------
- Read skill JSON files
- Convert dictionaries into Skill models
- Return strongly typed objects

This loader intentionally does NOT:
- Validate skills
- Build indexes
- Build relationships
- Store data
"""

from __future__ import annotations

from knowledge_builder.config import (
    SKILLS_DIRECTORY,
)
from knowledge_builder.loaders.base_loader import BaseLoader
from knowledge_builder.models import Skill


class SkillLoader(BaseLoader):
    """
    Loads normalized skills.
    """

    def load(self) -> list[Skill]:
        """
        Load every skill from the configured directory.

        Returns
        -------
        list[Skill]
        """
        skills: list[Skill] = []

        for file_path in self.list_json_files():
            data = self.read_json(file_path)

            if isinstance(data, dict):
                skills.append(
                    Skill.from_dict(data)
                )

            elif isinstance(data, list):
                skills.extend(
                    Skill.from_dict(item)
                    for item in data
                )

            else:
                raise TypeError(
                    f"Unsupported JSON structure in {file_path}"
                )

        skills.sort(
            key=lambda skill: skill.name.casefold()
        )

        return skills

    @classmethod
    def from_default_location(
        cls,
    ) -> "SkillLoader":
        """
        Create a loader using the default Knowledge Database location.
        """
        return cls(SKILLS_DIRECTORY)