"""
knowledge_builder.models.technology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Core technology model used throughout the ResumeOptimizer Knowledge Platform.

A Technology represents any technical skill or tool such as:

- Python
- FastAPI
- React
- Docker
- PostgreSQL
- AWS

This is the central model referenced by builders, analyzers,
planners, optimizers and AI prompt generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Technology:
    """
    Represents a technology.

    Attributes
    ----------
    id
        Unique identifier.

    name
        Display name.

    category_id
        Parent category id.

    description
        Short explanation.

    aliases
        Alternative names.

    related
        Related technology ids.

    keywords
        ATS keywords.

    deprecated
        Whether this technology should no longer be used.
    """

    id: str
    name: str
    category_id: str

    description: str = ""

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    related: Tuple[str, ...] = field(default_factory=tuple)

    keywords: Tuple[str, ...] = field(default_factory=tuple)

    deprecated: bool = False

    def matches(self, value: str) -> bool:
        """
        Check whether a value refers to this technology.

        Matching is case-insensitive.
        """
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def has_keyword(self, keyword: str) -> bool:
        """
        Returns True if keyword belongs to this technology.
        """
        normalized = keyword.strip().casefold()

        return normalized in (
            value.casefold()
            for value in self.keywords
        )

    def is_related_to(self, technology_id: str) -> bool:
        """
        Check relationship with another technology.
        """
        return technology_id in self.related

    def to_dict(self) -> dict:
        """
        Serialize object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "description": self.description,
            "aliases": list(self.aliases),
            "related": list(self.related),
            "keywords": list(self.keywords),
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Technology":
        """
        Deserialize object.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            category_id=data["category_id"],
            description=data.get("description", ""),
            aliases=tuple(data.get("aliases", [])),
            related=tuple(data.get("related", [])),
            keywords=tuple(data.get("keywords", [])),
            deprecated=data.get("deprecated", False),
        )