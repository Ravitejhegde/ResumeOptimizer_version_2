"""
knowledge_builder.models.ats_rule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents ATS optimization rules used by ResumeOptimizer.

Unlike technologies or skills, ATS rules define HOW a resume
should be optimized for Applicant Tracking Systems.

Examples
--------
Rule:
    Include required keywords naturally.

Rule:
    Do not stuff keywords.

Rule:
    Keep section headings standard.

Rule:
    Preserve chronological order.

Rule:
    Avoid tables for ATS compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Tuple


class ATSRuleSeverity(StrEnum):
    """
    Rule importance.
    """

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


@dataclass(slots=True, frozen=True)
class ATSRule:
    """
    Represents a single ATS optimization rule.

    Parameters
    ----------
    id
        Unique identifier.

    title
        Short rule name.

    description
        Explanation of the rule.

    severity
        Rule priority.

    category
        Rule category.

    applies_to_sections
        Resume sections affected.

    related_keyword_ids
        Keywords associated with the rule.

    enabled
        Whether the rule is active.
    """

    id: str

    title: str

    description: str

    severity: ATSRuleSeverity

    category: str

    applies_to_sections: Tuple[str, ...] = field(default_factory=tuple)

    related_keyword_ids: Tuple[str, ...] = field(default_factory=tuple)

    enabled: bool = True

    def applies_to(self, section_id: str) -> bool:
        """
        Returns True if this rule applies to
        the supplied resume section.
        """
        return section_id in self.applies_to_sections

    def is_critical(self) -> bool:
        """
        Returns True if the rule is critical.
        """
        return self.severity == ATSRuleSeverity.CRITICAL

    def to_dict(self) -> dict:
        """
        Serialize ATSRule.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category,
            "applies_to_sections": list(self.applies_to_sections),
            "related_keyword_ids": list(self.related_keyword_ids),
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ATSRule":
        """
        Deserialize ATSRule.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            severity=ATSRuleSeverity(data["severity"]),
            category=data["category"],
            applies_to_sections=tuple(
                data.get("applies_to_sections", [])
            ),
            related_keyword_ids=tuple(
                data.get("related_keyword_ids", [])
            ),
            enabled=bool(data.get("enabled", True)),
        )