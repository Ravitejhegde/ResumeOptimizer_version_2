from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisResult:
    """
    Unified analysis result produced by the
    Document Analyzer.

    Every analyzer contributes information to
    this object.
    """

    detected_role: str | None = None

    experience_level: str | None = None

    ats_score: float = 0.0

    technologies: list[str] = field(
        default_factory=list,
    )

    categorized_skills: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    matched_skills: list[str] = field(
        default_factory=list,
    )

    missing_skills: list[str] = field(
        default_factory=list,
    )

    related_skills: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )
