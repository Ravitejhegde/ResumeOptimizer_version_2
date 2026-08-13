"""
app.job_description.services.job_description_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses and analyzes a Job Description.
"""

from __future__ import annotations

from app.job_description.analyzers.role_analyzer import (
    RoleAnalyzer,
)
from app.job_description.analyzers.skill_analyzer import (
    SkillAnalyzer,
)
from app.job_description.analyzers.technology_analyzer import (
    TechnologyAnalyzer,
)
from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)


class JobDescriptionParser:
    """
    Parses and analyzes a Job Description.
    """

    def __init__(self) -> None:
        self._role = RoleAnalyzer()
        self._technology = TechnologyAnalyzer()
        self._skill = SkillAnalyzer()

    def parse(
        self,
        text: str,
    ) -> JobDescriptionModel:
        """
        Parse and analyze a Job Description.
        """

        model = JobDescriptionModel()

        model.text = text.strip()

        model.paragraphs = [
            paragraph.strip()
            for paragraph in text.splitlines()
            if paragraph.strip()
        ]

        # ---------------------------------
        # Analyze Roles
        # ---------------------------------

        model = self._role.analyze(
            model,
        )

        # ---------------------------------
        # Analyze Technologies
        # ---------------------------------

        model = self._technology.analyze(
            model,
        )

        # ---------------------------------
        # Analyze Skills
        # ---------------------------------

        model = self._skill.analyze(
            model,
        )

        return model