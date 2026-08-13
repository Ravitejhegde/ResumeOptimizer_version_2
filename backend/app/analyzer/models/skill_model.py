"""
app.analyzer.models.skill_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a detected engineering skill.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillModel:
    """
    Skill detected in the resume.
    """

    id: str

    name: str

    description: str = ""

    importance: int = 0

    technologies: set[str] = field(
        default_factory=set
    )

    sections: set[str] = field(
        default_factory=set
    )