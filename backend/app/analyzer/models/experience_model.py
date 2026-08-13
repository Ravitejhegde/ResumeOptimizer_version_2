"""
app.analyzer.models.experience_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a work experience entry.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExperienceModel:
    """
    Represents one work experience.
    """

    company: str = ""

    title: str = ""

    duration: str = ""

    description: list[str] = field(
        default_factory=list
    )

    technologies: set[str] = field(
        default_factory=set
    )

    skills: set[str] = field(
        default_factory=set
    )
    roles: set[str] = field(
        default_factory=set
    )