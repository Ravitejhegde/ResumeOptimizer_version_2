"""
knowledge_builder.models.category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Domain model representing a technology category.

A Category is the highest-level grouping within the ResumeOptimizer
Knowledge Platform.

Examples:
    - Programming Languages
    - Frameworks
    - Databases
    - Cloud Platforms
    - DevOps
    - AI / Machine Learning

Categories are immutable identifiers referenced throughout the
Knowledge Builder pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Category:
    """
    Represents a single technology category.

    Attributes
    ----------
    id:
        Unique identifier.
        Example:
            programming_languages

    name:
        Human-readable name.
        Example:
            Programming Languages

    description:
        Short explanation of the category.

    aliases:
        Alternative names used during normalization.
    """

    id: str
    name: str
    description: str = ""
    aliases: Tuple[str, ...] = field(default_factory=tuple)

    def matches(self, value: str) -> bool:
        """
        Returns True if the given value refers to this category.

        Matching is case-insensitive.

        Parameters
        ----------
        value:
            Category name or alias.

        Returns
        -------
        bool
        """
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def to_dict(self) -> dict:
        """
        Serialize the category.

        Returns
        -------
        dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "aliases": list(self.aliases),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """
        Create Category from dictionary.

        Raises
        ------
        KeyError
            If required keys are missing.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            aliases=tuple(data.get("aliases", [])),
        )