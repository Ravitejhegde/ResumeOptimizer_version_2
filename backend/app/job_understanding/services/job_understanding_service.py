"""
app.job_understanding.services.job_understanding_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for job understanding.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)

from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)

from app.job_understanding.role.role_understanding import (
    RoleUnderstanding,
)

from app.job_understanding.skill.skill_understanding import (
    SkillUnderstanding,
)

from app.job_understanding.technology.technology_understanding import (
    TechnologyUnderstanding,
)

from app.job_understanding.keyword.keyword_understanding import (
    KeywordUnderstanding,
)


class JobUnderstandingService:
    """
    Builds a complete understanding of a job description.
    """

    def __init__(self) -> None:

        self._role = RoleUnderstanding()
        self._skill = SkillUnderstanding()
        self._technology = TechnologyUnderstanding()
        self._keyword = KeywordUnderstanding()

    def understand(
        self,
        job: JobDescriptionModel,
    ) -> JobUnderstanding:

        understanding = JobUnderstanding()

        understanding = self._role.analyze(
            job,
            understanding,
        )

        understanding = self._skill.analyze(
            job,
            understanding,
        )

        understanding = self._technology.analyze(
            job,
            understanding,
        )

        understanding = self._keyword.analyze(
            job,
            understanding,
        )

        return understanding