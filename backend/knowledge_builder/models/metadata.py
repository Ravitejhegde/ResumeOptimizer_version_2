"""
knowledge_builder.models.metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Metadata describing a generated Knowledge Builder build.

This information is exported together with the generated knowledge
files so downstream modules (Analyzer, Planner, Optimizer, etc.)
can verify compatibility, detect stale builds and display build
information.

The metadata model intentionally contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Tuple


@dataclass(slots=True, frozen=True)
class BuildMetadata:
    """
    Metadata for a completed Knowledge Builder build.

    Parameters
    ----------
    version
        Knowledge schema version.

    build_number
        Incremental build number.

    generated_at
        UTC timestamp.

    source_count
        Number of loaded source files.

    category_count
        Number of categories.

    technology_count
        Number of technologies.

    skill_count
        Number of skills.

    role_count
        Number of roles.

    section_count
        Number of sections.

    keyword_count
        Number of keywords.

    relationship_count
        Number of relationships.

    ats_rule_count
        Number of ATS rules.

    warnings
        Non-fatal validation warnings.

    notes
        Optional build notes.
    """

    version: str

    build_number: int

    generated_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    source_count: int = 0

    category_count: int = 0

    technology_count: int = 0

    skill_count: int = 0

    role_count: int = 0

    section_count: int = 0

    keyword_count: int = 0

    relationship_count: int = 0

    ats_rule_count: int = 0

    warnings: Tuple[str, ...] = field(default_factory=tuple)

    notes: str = ""

    @property
    def total_entities(self) -> int:
        """
        Total knowledge entities generated.
        """
        return (
            self.category_count
            + self.technology_count
            + self.skill_count
            + self.role_count
            + self.section_count
            + self.keyword_count
            + self.relationship_count
            + self.ats_rule_count
        )

    @property
    def has_warnings(self) -> bool:
        """
        Returns True when validation produced warnings.
        """
        return bool(self.warnings)

    def to_dict(self) -> dict:
        """
        Serialize metadata.
        """
        return {
            "version": self.version,
            "build_number": self.build_number,
            "generated_at": self.generated_at,
            "source_count": self.source_count,
            "category_count": self.category_count,
            "technology_count": self.technology_count,
            "skill_count": self.skill_count,
            "role_count": self.role_count,
            "section_count": self.section_count,
            "keyword_count": self.keyword_count,
            "relationship_count": self.relationship_count,
            "ats_rule_count": self.ats_rule_count,
            "total_entities": self.total_entities,
            "warnings": list(self.warnings),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BuildMetadata":
        """
        Deserialize metadata.
        """
        return cls(
            version=data["version"],
            build_number=int(data["build_number"]),
            generated_at=data.get(
                "generated_at",
                datetime.now(timezone.utc).isoformat(),
            ),
            source_count=int(data.get("source_count", 0)),
            category_count=int(data.get("category_count", 0)),
            technology_count=int(data.get("technology_count", 0)),
            skill_count=int(data.get("skill_count", 0)),
            role_count=int(data.get("role_count", 0)),
            section_count=int(data.get("section_count", 0)),
            keyword_count=int(data.get("keyword_count", 0)),
            relationship_count=int(
                data.get("relationship_count", 0)
            ),
            ats_rule_count=int(data.get("ats_rule_count", 0)),
            warnings=tuple(data.get("warnings", [])),
            notes=data.get("notes", ""),
        )