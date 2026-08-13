"""
app.analyzer.models.document_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a parsed resume document.

This model is the foundation of the Resume Analyzer.
Every analyzer works with this object instead of raw
DOCX documents.
"""

from __future__ import annotations
from app.analyzer.models.skill_model import (
    SkillModel,
)
from app.analyzer.models.experience_model import (
    ExperienceModel,
)
from app.analyzer.models.technology_model import (
    TechnologyModel,
)
from dataclasses import dataclass, field
from app.analyzer.models.technology_model import (
    TechnologyModel,
)
from app.analyzer.models.role_model import (
    RoleModel,
)
from app.analyzer.models.project_model import (
        ProjectModel,
)


@dataclass(slots=True)
class DocumentModel:
    """
    Parsed resume document.
    """

    filename: str = ""

    text: str = ""

    paragraphs: list[str] = field(default_factory=list)

    sections: dict[str, list[str]] = field(
        default_factory=dict
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )
    technologies: dict[str, "TechnologyModel"] = field(
        default_factory=dict
    )
    skills: dict[str, SkillModel] = field(
        default_factory=dict
    )
    roles: dict[str, RoleModel] = field(
        default_factory=dict
    )    
    experiences: list[ExperienceModel] = field(
        default_factory=list
    )
    
    projects: list[ProjectModel] = field(
    default_factory=list
)


    @property
    def is_empty(self) -> bool:
        """
        True if the document has no text.
        """
        return not self.text.strip()

    @property
    def paragraph_count(self) -> int:
        """
        Number of paragraphs.
        """
        return len(self.paragraphs)

    @property
    def section_count(self) -> int:
        """
        Number of detected sections.
        """
        return len(self.sections)