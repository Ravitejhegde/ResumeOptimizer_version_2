"""
app.job_understanding.models.job_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semantic understanding of a Job Description.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class JobUnderstanding:
    """
    High-level understanding of a job description.
    """

    target_role: str = ""

    required_skills: list[str] = field(
        default_factory=list
    )

    required_technologies: list[str] = field(
        default_factory=list
    )

    required_keywords: list[str] = field(
        default_factory=list
    )

    preferred_skills: list[str] = field(
        default_factory=list
    )

    seniority: str = ""

    summary: str = ""