"""
app.job_description.analyzers.skill_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detects skills mentioned or implied in a JobDescription.
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

        text = job.text.casefold()

        job.skills.clear()

        for skill in self._skills.all():

            name = skill["name"].casefold()

            if name in text:
                self._add_skill(job, skill)
                continue

            aliases = [
                alias.casefold()
                for alias in skill.get("aliases", [])
            ]

            if any(alias in text for alias in aliases):
                self._add_skill(job, skill)
                continue

            keywords = [
                keyword.casefold()
                for keyword in skill.get("keywords", [])
                if keyword.strip()
            ]

            matched_keywords = {
                keyword
                for keyword in keywords
                if keyword in text
            }

            if len(matched_keywords) >= 2:
                self._add_skill(job, skill)

        return job

    @staticmethod
    def _add_skill(
        job: JobDescriptionModel,
        skill: dict,
    ) -> None:
        model = SkillModel(
            id=skill["id"],
            name=skill["name"],
        )

        job.skills[model.id] = model