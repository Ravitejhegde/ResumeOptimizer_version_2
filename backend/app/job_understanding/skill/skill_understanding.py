"""
app.job_understanding.skill.skill_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines required skills.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


class SkillUnderstanding:

    def analyze(
        self,
        job: JobDescriptionModel,
        understanding: JobUnderstanding,
    ) -> JobUnderstanding:

        understanding.required_skills = sorted(
            skill.name
            for skill in job.skills.values()
        )

        return understanding