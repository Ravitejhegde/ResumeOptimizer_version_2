"""
app.job_description.analyzers.skill_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detects skills mentioned or implied in a Job Description.
"""

from __future__ import annotations

from app.analyzer.models.skill_model import (
    SkillModel,
)
from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.knowledge.provider import (
    get_knowledge,
)


class SkillAnalyzer:
    """
    Detects skills from a Job Description.
    """

    def __init__(self) -> None:
        self._skills = get_knowledge().skills

    def analyze(
        self,
        job: JobDescriptionModel,
    ) -> JobDescriptionModel:
        """
        Populate job.skills.
        """

        text = job.text.lower()

        job.skills.clear()

        for skill in self._skills.all():

            name = skill["name"].lower()

            if name in text:

                model = SkillModel(
                    id=skill["id"],
                    name=skill["name"],
                )

                job.skills[
                    model.id
                ] = model

        return job