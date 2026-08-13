"""
app.job_description.models.job_description_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a parsed Job Description.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.analyzer.models.role_model import (
    RoleModel,
)
from app.analyzer.models.skill_model import (
    SkillModel,
)
from app.analyzer.models.technology_model import (
    TechnologyModel,
)


@dataclass(slots=True)
class JobDescriptionModel:
    """
    Parsed Job Description.
    """

    text: str = ""

    paragraphs: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    technologies: dict[str, TechnologyModel] = field(
        default_factory=dict
    )

    skills: dict[str, SkillModel] = field(
        default_factory=dict
    )

    roles: dict[str, RoleModel] = field(
        default_factory=dict
    )

    @property
    def is_empty(self) -> bool:
        return not self.text.strip()