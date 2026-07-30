"""
knowledge_builder.models.synonym
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized synonym mapping.

The ResumeOptimizer Knowledge Platform uses synonym mappings to
normalize different words that mean the same thing.

Examples
--------
Artificial Intelligence
    -> AI

Javascript
    -> JavaScript

Node
    -> Node.js

Postgres
    -> PostgreSQL

Git Hub
    -> GitHub

These mappings improve:

- Resume analysis
- Job description parsing
- Skill matching
- ATS keyword detection
- AI prompt quality
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Synonym:
    """
    Represents a canonical term and its aliases.

    Parameters
    ----------
    id
        Unique identifier.

    canonical
        Official normalized value.

    aliases
        Alternative spellings or names.

    description
        Optional explanation.

    case_sensitive
        Whether matching should respect case.
    """

    id: str

    canonical: str

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    description: str = ""

    case_sensitive: bool = False

    def normalize(self, value: str) -> str:
        """
        Normalize a value.

        Returns the canonical value if the supplied
        value matches either the canonical term or
        one of its aliases.

        Otherwise returns the original value.
        """
        candidate = value.strip()

        if self.case_sensitive:
            if candidate == self.canonical:
                return self.canonical

            if candidate in self.aliases:
                return self.canonical

            return value

        normalized = candidate.casefold()

        if normalized == self.canonical.casefold():
            return self.canonical

        for alias in self.aliases:
            if normalized == alias.casefold():
                return self.canonical

        return value

    def matches(self, value: str) -> bool:
        """
        Returns True if the supplied value belongs
        to this synonym group.
        """
        return self.normalize(value) == self.canonical

    def to_dict(self) -> dict:
        """
        Serialize Synonym.
        """
        return {
            "id": self.id,
            "canonical": self.canonical,
            "aliases": list(self.aliases),
            "description": self.description,
            "case_sensitive": self.case_sensitive,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Synonym":
        """
        Deserialize Synonym.
        """
        return cls(
            id=data["id"],
            canonical=data["canonical"],
            aliases=tuple(data.get("aliases", [])),
            description=data.get("description", ""),
            case_sensitive=bool(data.get("case_sensitive", False)),
        )