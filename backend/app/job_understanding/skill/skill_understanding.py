"""
app.job_understanding.skill.skill_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines required competency skills.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)
from app.knowledge.provider import (
    get_knowledge,
)


class SkillUnderstanding:

    def __init__(self) -> None:
        self._knowledge = get_knowledge()

    def analyze(
        self,
        job: JobDescriptionModel,
        understanding: JobUnderstanding,
    ) -> JobUnderstanding:

        required_skills = []

        for skill in job.skills.values():

            # Technology-backed skill records are handled
            # by TechnologyUnderstanding.
            if self._knowledge.technologies.exists(skill.id):
                continue

            required_skills.append(skill.name)

        understanding.required_skills = sorted(
            required_skills
        )

        return understanding