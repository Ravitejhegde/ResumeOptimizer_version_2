"""
app.analyzer.models.project_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a resume project.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProjectModel:
    """
    Represents one project.
    """

    name: str = ""

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