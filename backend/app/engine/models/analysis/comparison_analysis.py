from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ComparisonAnalysis:
    """
    Resume vs Job Description comparison.
    """

    matched: list[str] = field(
        default_factory=list,
    )

    missing: list[str] = field(
        default_factory=list,
    )

    extra: list[str] = field(
        default_factory=list,
    )

    related: list[str] = field(
        default_factory=list,
    )

    score: float = 0.0
