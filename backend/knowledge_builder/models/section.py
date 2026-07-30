"""
knowledge_builder.models.section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized resume section.

A Section defines the standard structure of a professional resume.

Examples
--------
- Summary
- Experience
- Education
- Skills
- Projects
- Certifications
- Achievements

These definitions help ResumeOptimizer understand
where information belongs and which sections are
recommended for different job roles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(slots=True, frozen=True)
class Section:
    """
    Represents a normalized resume section.

    Parameters
    ----------
    id
        Unique identifier.

    name
        Display name.

    description
        Description of the section.

    aliases
        Alternative section names found in resumes.

    required
        Whether this section is generally required.

    recommended_order
        Suggested ordering in the final resume.

    ats_weight
        Relative ATS importance (1-10).

    deprecated
        Whether the section is obsolete.
    """

    id: str
    name: str

    description: str = ""

    aliases: Tuple[str, ...] = field(default_factory=tuple)

    required: bool = False

    recommended_order: int = 0

    ats_weight: int = 5

    deprecated: bool = False

    def matches(self, value: str) -> bool:
        """
        Returns True if the given value refers
        to this section.
        """
        normalized = value.strip().casefold()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def is_required(self) -> bool:
        """
        Indicates whether the section is required.
        """
        return self.required

    def to_dict(self) -> dict:
        """
        Serialize section.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "aliases": list(self.aliases),
            "required": self.required,
            "recommended_order": self.recommended_order,
            "ats_weight": self.ats_weight,
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Section":
        """
        Deserialize section.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            aliases=tuple(data.get("aliases", [])),
            required=bool(data.get("required", False)),
            recommended_order=int(data.get("recommended_order", 0)),
            ats_weight=int(data.get("ats_weight", 5)),
            deprecated=bool(data.get("deprecated", False)),
        )