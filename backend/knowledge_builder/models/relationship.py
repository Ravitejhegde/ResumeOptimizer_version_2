"""
knowledge_builder.models.relationship
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a semantic relationship between two knowledge entities.

Relationships are the foundation of ResumeOptimizer's reasoning engine.

Examples
--------
Python ----USES------> FastAPI
FastAPI ---REQUIRES--> Python
Docker ----RELATED---> Kubernetes
TensorFlow-CHILD_OF--> Machine Learning
React -----ALIAS_OF--> ReactJS

The Knowledge Builder generates these relationships and later the
Analyzer, Planner and Prompt Engine use them to understand how
technologies are connected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RelationshipType(StrEnum):
    """
    Supported relationship types.
    """

    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"

    RELATED_TO = "related_to"

    USES = "uses"

    REQUIRES = "requires"

    DEPENDS_ON = "depends_on"

    BELONGS_TO = "belongs_to"

    SIMILAR_TO = "similar_to"

    RECOMMENDED_WITH = "recommended_with"

    ALIAS_OF = "alias_of"


@dataclass(slots=True, frozen=True)
class Relationship:
    """
    Represents a directed relationship between two entities.

    Example
    -------
    source_id:
        fastapi

    relationship:
        REQUIRES

    target_id:
        python
    """

    source_id: str

    relationship: RelationshipType

    target_id: str

    weight: float = 1.0

    bidirectional: bool = False

    description: str = ""

    def reverse(self) -> "Relationship":
        """
        Create the reverse relationship.

        Useful when building graph indexes.
        """
        return Relationship(
            source_id=self.target_id,
            relationship=self.relationship,
            target_id=self.source_id,
            weight=self.weight,
            bidirectional=self.bidirectional,
            description=self.description,
        )

    def connects(self, entity_id: str) -> bool:
        """
        Returns True if the entity participates
        in this relationship.
        """
        return entity_id in (self.source_id, self.target_id)

    def to_dict(self) -> dict:
        """
        Serialize relationship.
        """
        return {
            "source_id": self.source_id,
            "relationship": self.relationship.value,
            "target_id": self.target_id,
            "weight": self.weight,
            "bidirectional": self.bidirectional,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Relationship":
        """
        Deserialize relationship.
        """
        return cls(
            source_id=data["source_id"],
            relationship=RelationshipType(data["relationship"]),
            target_id=data["target_id"],
            weight=float(data.get("weight", 1.0)),
            bidirectional=bool(data.get("bidirectional", False)),
            description=data.get("description", ""),
        )