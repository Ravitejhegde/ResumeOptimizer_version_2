"""
app.understanding.services.resume_understanding_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for resume understanding.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)

from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)

from app.understanding.role.role_understanding import (
    RoleUnderstanding,
)
from app.understanding.skill.skill_understanding import (
    SkillUnderstanding,
)
from app.understanding.technology.technology_understanding import (
    TechnologyUnderstanding,
)
from app.understanding.experience.experience_understanding import (
    ExperienceUnderstanding,
)
from app.understanding.project.project_understanding import (
    ProjectUnderstanding,
)
from app.understanding.summary_understanding import (
    SummaryUnderstanding,
)


class ResumeUnderstandingService:
    """
    Builds a complete understanding of a resume.
    """

    def __init__(self) -> None:

        self._role = RoleUnderstanding()
        self._skill = SkillUnderstanding()
        self._technology = TechnologyUnderstanding()
        self._experience = ExperienceUnderstanding()
        self._project = ProjectUnderstanding()
        self._summary = SummaryUnderstanding()

    def understand(
        self,
        document: DocumentModel,
    ) -> ResumeUnderstanding:

        understanding = ResumeUnderstanding()

        understanding = self._role.analyze(
            document,
            understanding,
        )

        understanding = self._skill.analyze(
            document,
            understanding,
        )

        understanding = self._technology.analyze(
            document,
            understanding,
        )

        understanding = self._experience.analyze(
            document,
            understanding,
        )

        understanding = self._project.analyze(
            document,
            understanding,
        )

        understanding = self._summary.analyze(
            document,
            understanding,
        )

        return understanding