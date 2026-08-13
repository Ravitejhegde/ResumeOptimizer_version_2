"""
knowledge_builder.models.technology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Core technology model used throughout the ResumeOptimizer Knowledge Platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Technology:
    """
    Represents a technology.
    """

    id: str

    name: str

    category_id: str

    description: str = ""

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    related: Tuple[str, ...] = field(default_factory=tuple)

    keywords: Tuple[str, ...] = field(default_factory=tuple)

    deprecated: bool = False

    official_url: str | None = None

    tags: Tuple[str, ...] = field(default_factory=tuple)

    @property
    def related_technology_ids(self) -> Tuple[str, ...]:
        """
        Backward-compatible alias expected by builders.
        """
        return self.related

    @property
    def keyword_ids(self) -> Tuple[str, ...]:
        """
        Backward-compatible alias expected by builders.
        """
        return self.keywords

    def matches(self, value: str) -> bool:
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def has_keyword(self, keyword: str) -> bool:
        normalized = keyword.strip().casefold()

        return normalized in (
            value.casefold()
            for value in self.keywords
        )

    def is_related_to(self, technology_id: str) -> bool:
        return technology_id in self.related

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "description": self.description,
            "aliases": list(self.aliases),
            "related": list(self.related),
            "keywords": list(self.keywords),
            "deprecated": self.deprecated,
            "official_url": self.official_url,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "Technology":
        return cls(
            id=data["id"],
            name=data["name"],
            category_id=data["category_id"],
            description=data.get("description", ""),
            aliases=tuple(data.get("aliases", [])),
            related=tuple(data.get("related", [])),
            keywords=tuple(data.get("keywords", [])),
            deprecated=bool(data.get("deprecated", False)),
            official_url=data.get("official_url"),
            tags=tuple(data.get("tags", [])),
        )