"""
app.understanding.models.resume_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semantic understanding of a resume.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ResumeUnderstanding:
    """
    High-level semantic understanding of a resume.
    """

    primary_role: str = ""

    secondary_roles: list[str] = field(
        default_factory=list
    )

    primary_technologies: list[str] = field(
        default_factory=list
    )

    primary_skills: list[str] = field(
        default_factory=list
    )

    strongest_experience: str = ""

    strongest_project: str = ""

    strengths: list[str] = field(
        default_factory=list
    )

    weaknesses: list[str] = field(
        default_factory=list
    )

    seniority: str = ""

    summary: str = ""