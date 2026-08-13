"""
app.planner.evidence.evidence_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collection of evidence results.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.planner.evidence.evidence_item import (
    EvidenceItem,
)


@dataclass(slots=True)
class EvidenceReport:
    """
    Complete evidence analysis.
    """

    items: list[EvidenceItem] = field(
        default_factory=list
    )

    @property
    def supported(self) -> list[EvidenceItem]:
        return [
            item
            for item in self.items
            if item.supported
        ]

    @property
    def unsupported(self) -> list[EvidenceItem]:
        return [
            item
            for item in self.items
            if not item.supported
        ]