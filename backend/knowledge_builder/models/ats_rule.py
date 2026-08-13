"""
knowledge_builder.models.ats_rule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents an ATS optimization rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ATSRulePriority(StrEnum):
    """
    ATS rule priority.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True, frozen=True)
class ATSRule:
    """
    Represents a single ATS optimization rule.
    """

    id: str

    name: str

    category: str

    priority: ATSRulePriority

    description: str

    score: int = 0

    def is_critical(self) -> bool:
        """
        Returns True if this is a critical rule.
        """
        return self.priority == ATSRulePriority.CRITICAL

    def to_dict(self) -> dict:
        """
        Serialize ATSRule.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "priority": self.priority.value,
            "description": self.description,
            "score": self.score,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ATSRule":
        """
        Deserialize ATSRule.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            priority=ATSRulePriority(
                data["priority"]
            ),
            description=data.get(
                "description",
                "",
            ),
            score=int(
                data.get("score", 0)
            ),
        )