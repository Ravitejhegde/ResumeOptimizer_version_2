"""
app.evidence.models.evidence_item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents evidence supporting a planner decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EvidenceItem:
    """
    Evidence collected for one optimization target.
    """

    id: str = ""

    type: str = ""

    target: str = ""

    supported: bool = False

    confidence: float = 0.0

    matched_resume_skills: list[str] = field(
        default_factory=list
    )

    matched_resume_technologies: list[str] = field(
        default_factory=list
    )

    evidence_sources: list[str] = field(
        default_factory=list
    )

    reasoning: list[str] = field(
        default_factory=list
    )

    recommended_action: str = ""

    reason: str = ""