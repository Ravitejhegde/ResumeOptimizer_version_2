"""
app.understanding.services.understanding_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a semantic understanding from a DocumentModel.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.experience.experience_understanding import (
    ExperienceUnderstanding,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)
from app.understanding.project.project_understanding import (
    ProjectUnderstanding,
)
from app.understanding.role.role_understanding import (
    RoleUnderstanding,
)
from app.understanding.skill.skill_understanding import (
    SkillUnderstanding,
)
from app.understanding.summary_understanding import (
    SummaryUnderstanding,
)
from app.understanding.technology.technology_understanding import (
    TechnologyUnderstanding,
)


class UnderstandingBuilder:
    """
    Builds a ResumeUnderstanding from a DocumentModel.
    """

    def __init__(self) -> None:
        self._role = RoleUnderstanding()
        self._technology = TechnologyUnderstanding()
        self._skill = SkillUnderstanding()
        self._experience = ExperienceUnderstanding()
        self._project = ProjectUnderstanding()
        self._summary = SummaryUnderstanding()

    def build(
        self,
        document: DocumentModel,
    ) -> ResumeUnderstanding:
        """
        Build a semantic understanding of the resume.
        """

        understanding = ResumeUnderstanding()

        # -------------------------------------------------
        # Role Understanding
        # -------------------------------------------------

        understanding = self._role.analyze(
            document,
            understanding,
        )

        # -------------------------------------------------
        # Technology Understanding
        # -------------------------------------------------

        understanding = self._technology.analyze(
            document,
            understanding,
        )

        # -------------------------------------------------
        # Skill Understanding
        # -------------------------------------------------

        understanding = self._skill.analyze(
            document,
            understanding,
        )

        # -------------------------------------------------
        # Experience Understanding
        # -------------------------------------------------

        understanding = self._experience.analyze(
            document,
            understanding,
        )

        # -------------------------------------------------
        # Project Understanding
        # -------------------------------------------------

        understanding = self._project.analyze(
            document,
            understanding,
        )

        # -------------------------------------------------
        # Resume Summary
        # -------------------------------------------------

        understanding = self._summary.analyze(
            document,
            understanding,
        )

        return understanding