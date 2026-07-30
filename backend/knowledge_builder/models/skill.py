"""
knowledge_builder.models.skill
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized resume skill.

Unlike Technology, a Skill is broader and describes an ability,
competency or knowledge area.

Examples
--------
Technology:
    - FastAPI
    - PostgreSQL
    - Docker

Skill:
    - Backend Development
    - REST API Development
    - Database Design
    - Machine Learning
    - Problem Solving

Multiple technologies may contribute to a single skill.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Skill:
    """
    Represents a normalized skill.

    Parameters
    ----------
    id
        Unique identifier.

    name
        Display name.

    description
        Human readable description.

    technology_ids
        Technologies associated with this skill.

    aliases
        Alternative names.

    keywords
        ATS keywords.

    importance
        Relative importance (1-10).

    deprecated
        Indicates whether this skill should be ignored in future datasets.
    """

    id: str
    name: str

    description: str = ""

    technology_ids: Tuple[str, ...] = field(default_factory=tuple)

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    keywords: Tuple[str, ...] = field(default_factory=tuple)

    importance: int = 5

    deprecated: bool = False

    def matches(self, value: str) -> bool:
        """
        Returns True if the supplied value refers to this skill.
        """
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def has_technology(self, technology_id: str) -> bool:
        """
        Returns True if the technology belongs to this skill.
        """
        return technology_id in self.technology_ids

    def has_keyword(self, keyword: str) -> bool:
        """
        Returns True if keyword belongs to this skill.
        """
        normalized = keyword.strip().casefold()

        return normalized in (
            value.casefold()
            for value in self.keywords
        )

    def to_dict(self) -> dict:
        """
        Serialize Skill.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "technology_ids": list(self.technology_ids),
            "aliases": list(self.aliases),
            "keywords": list(self.keywords),
            "importance": self.importance,
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Skill":
        """
        Deserialize Skill.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            technology_ids=tuple(data.get("technology_ids", [])),
            aliases=tuple(data.get("aliases", [])),
            keywords=tuple(data.get("keywords", [])),
            importance=int(data.get("importance", 5)),
            deprecated=bool(data.get("deprecated", False)),
        )