"""
app.planner.evidence.evidence_item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents evidence for one optimization item.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EvidenceItem:
    """
    Evidence supporting an optimization.
    """

    id: str

    type: str

    supported: bool

    confidence: float

    evidence_sources: list[str] = field(
        default_factory=list
    )

    reasoning: list[str] = field(
        default_factory=list
    )

    recommended_action: str = ""