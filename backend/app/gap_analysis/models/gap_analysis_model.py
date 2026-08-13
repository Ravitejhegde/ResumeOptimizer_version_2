"""
app.gap_analysis.models.gap_analysis_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the semantic gap between a resume and a job description.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GapAnalysisModel:
    """
    Semantic comparison between a resume and a job description.
    """

    role_match: float = 0.0

    skill_match: float = 0.0

    technology_match: float = 0.0

    experience_match: float = 0.0

    project_match: float = 0.0

    ats_match: float = 0.0

    overall_match: float = 0.0

    matched_skills: list[str] = field(
        default_factory=list
    )

    missing_skills: list[str] = field(
        default_factory=list
    )

    matched_technologies: list[str] = field(
        default_factory=list
    )

    missing_technologies: list[str] = field(
        default_factory=list
    )

    matched_keywords: list[str] = field(
        default_factory=list
    )

    missing_keywords: list[str] = field(
        default_factory=list
    )

    strengths: list[str] = field(
        default_factory=list
    )

    weaknesses: list[str] = field(
        default_factory=list
    )

    rewrite_sections: list[str] = field(
        default_factory=list
    )