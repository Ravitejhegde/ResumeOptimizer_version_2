"""
app.analyzer.services.resume_analysis_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Orchestrates resume analysis stages.
"""

from __future__ import annotations

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)
from app.analyzer.document.section_analyzer import (
    SectionAnalyzer,
)
from app.analyzer.role.role_analyzer import (
    RoleAnalyzer,
)
from app.analyzer.skill.skill_analyzer import (
    SkillAnalyzer,
)
from app.analyzer.technology.technology_analyzer import (
    TechnologyAnalyzer,
)
from app.analyzer.experience.experience_analyzer import (
    ExperienceAnalyzer,
)
from app.analyzer.project.project_analyzer import (
    ProjectAnalyzer,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)


class ResumeAnalysisService:
    """
    Orchestrates the complete resume analysis pipeline.
    """

    def __init__(self) -> None:
        self._document = DocumentAnalyzer()
        self._section = SectionAnalyzer()
        self._role = RoleAnalyzer()
        self._skill = SkillAnalyzer()
        self._technology = TechnologyAnalyzer()
        self._experience = ExperienceAnalyzer()
        self._project = ProjectAnalyzer()

    def analyze(
        self,
        document: str,
    ) -> DocumentModel:
        """
        Execute resume analysis stages in dependency order.
        """

        result = self._document.analyze(document)

        result = self._section.analyze(result)

        result = self._technology.analyze(result)
        result = self._skill.analyze(result)
        result = self._role.analyze(result)

        result = self._experience.analyze(result)
        result = self._project.analyze(result)

        return result