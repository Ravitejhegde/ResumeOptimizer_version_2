"""
knowledge_builder.models.role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized job role within the ResumeOptimizer
Knowledge Platform.

Examples
--------
- Backend Developer
- Frontend Developer
- Full Stack Developer
- DevOps Engineer
- Machine Learning Engineer
- Data Scientist

A Role is the bridge between Job Descriptions and the Knowledge
Platform. It defines the expected skills, technologies, keywords,
resume sections and optimization priorities for a profession.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Role:
    """
    Represents a normalized job role.

    Parameters
    ----------
    id
        Unique identifier.

    name
        Display name.

    description
        Human-readable description.

    aliases
        Alternative names.

    technology_ids
        Recommended technologies.

    skill_ids
        Required skills.

    keyword_ids
        ATS keyword identifiers.

    section_ids
        Recommended resume sections.

    priority_keywords
        High-priority ATS keywords.

    deprecated
        Indicates whether the role should no longer be used.
    """

    id: str
    name: str

    description: str = ""

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    technology_ids: Tuple[str, ...] = field(default_factory=tuple)

    skill_ids: Tuple[str, ...] = field(default_factory=tuple)

    keyword_ids: Tuple[str, ...] = field(default_factory=tuple)

    section_ids: Tuple[str, ...] = field(default_factory=tuple)

    priority_keywords: Tuple[str, ...] = field(default_factory=tuple)

    deprecated: bool = False

    def matches(self, value: str) -> bool:
        """
        Returns True if the supplied value refers to this role.
        """
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def requires_skill(self, skill_id: str) -> bool:
        """
        Returns True if the role requires the given skill.
        """
        return skill_id in self.skill_ids

    def uses_technology(self, technology_id: str) -> bool:
        """
        Returns True if the role commonly uses the technology.
        """
        return technology_id in self.technology_ids

    def recommends_section(self, section_id: str) -> bool:
        """
        Returns True if the resume section is recommended.
        """
        return section_id in self.section_ids

    def to_dict(self) -> dict:
        """
        Serialize Role.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "aliases": list(self.aliases),
            "technology_ids": list(self.technology_ids),
            "skill_ids": list(self.skill_ids),
            "keyword_ids": list(self.keyword_ids),
            "section_ids": list(self.section_ids),
            "priority_keywords": list(self.priority_keywords),
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Role":
        """
        Deserialize Role.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            aliases=tuple(data.get("aliases", [])),
            technology_ids=tuple(data.get("technology_ids", [])),
            skill_ids=tuple(data.get("skill_ids", [])),
            keyword_ids=tuple(data.get("keyword_ids", [])),
            section_ids=tuple(data.get("section_ids", [])),
            priority_keywords=tuple(data.get("priority_keywords", [])),
            deprecated=bool(data.get("deprecated", False)),
        )