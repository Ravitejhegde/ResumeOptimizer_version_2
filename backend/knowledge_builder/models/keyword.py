"""
knowledge_builder.models.keyword
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized ATS keyword.

Keywords are not technologies themselves.
Instead, they are searchable terms commonly used by
Applicant Tracking Systems (ATS).

Examples
--------
Technology:
    FastAPI

Keyword:
    REST API
    Backend Development
    API Development

A keyword may belong to one or more technologies,
skills or job roles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Keyword:
    """
    Represents a normalized ATS keyword.

    Parameters
    ----------
    id
        Unique identifier.

    value
        Canonical keyword.

    aliases
        Alternative spellings.

    technology_ids
        Related technologies.

    skill_ids
        Related skills.

    role_ids
        Related job roles.

    importance
        Relative ATS importance (1-10).

    description
        Human readable description.
    """

    id: str

    value: str

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    technology_ids: Tuple[str, ...] = field(default_factory=tuple)

    skill_ids: Tuple[str, ...] = field(default_factory=tuple)

    role_ids: Tuple[str, ...] = field(default_factory=tuple)

    importance: int = 5

    description: str = ""

    deprecated: bool = False

    def matches(self, text: str) -> bool:
        """
        Returns True if the supplied text matches
        this keyword.
        """
        normalized = text.strip().casefold()

        if normalized == self.value.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def belongs_to_role(self, role_id: str) -> bool:
        """
        Returns True if keyword belongs to the role.
        """
        return role_id in self.role_ids

    def belongs_to_skill(self, skill_id: str) -> bool:
        """
        Returns True if keyword belongs to the skill.
        """
        return skill_id in self.skill_ids

    def belongs_to_technology(self, technology_id: str) -> bool:
        """
        Returns True if keyword belongs to the technology.
        """
        return technology_id in self.technology_ids

    def to_dict(self) -> dict:
        """
        Serialize Keyword.
        """
        return {
            "id": self.id,
            "value": self.value,
            "aliases": list(self.aliases),
            "technology_ids": list(self.technology_ids),
            "skill_ids": list(self.skill_ids),
            "role_ids": list(self.role_ids),
            "importance": self.importance,
            "description": self.description,
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Keyword":
        """
        Deserialize Keyword.
        """
        return cls(
            id=data["id"],
            value=data["value"],
            aliases=tuple(data.get("aliases", [])),
            technology_ids=tuple(data.get("technology_ids", [])),
            skill_ids=tuple(data.get("skill_ids", [])),
            role_ids=tuple(data.get("role_ids", [])),
            importance=int(data.get("importance", 5)),
            description=data.get("description", ""),
            deprecated=bool(data.get("deprecated", False)),
        )