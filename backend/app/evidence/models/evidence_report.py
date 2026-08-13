"""
app.evidence.models.evidence_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Evidence report produced after gap analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.evidence.models.evidence_item import (
    EvidenceItem,
)


@dataclass(slots=True)
class EvidenceReport:
    """
    Complete evidence report.
    """

    items: list[EvidenceItem] = field(
        default_factory=list
    )

    safe_targets: list[str] = field(
        default_factory=list
    )

    unsafe_targets: list[str] = field(
        default_factory=list
    )