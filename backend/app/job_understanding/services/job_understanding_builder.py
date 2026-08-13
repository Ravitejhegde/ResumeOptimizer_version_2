"""
app.job_understanding.services.job_understanding_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a semantic understanding of a Job Description.
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


class JobUnderstandingBuilder:
    """
    Builds JobUnderstanding.
    """

    def __init__(self) -> None:
        self._role = RoleUnderstanding()
        self._skill = SkillUnderstanding()
        self._technology = TechnologyUnderstanding()
        self._keyword = KeywordUnderstanding()

    def build(
        self,
        job: JobDescriptionModel,
    ) -> JobUnderstanding:

        understanding = JobUnderstanding()

        understanding = self._role.analyze(
            job,
            understanding,
        )

        understanding = self._technology.analyze(
            job,
            understanding,
        )

        understanding = self._skill.analyze(
            job,
            understanding,
        )

        understanding = self._keyword.analyze(
            job,
            understanding,
        )

        understanding.summary = (
            f"{understanding.target_role} "
            f"requiring "
            f"{len(understanding.required_skills)} skills."
        )

        return understanding