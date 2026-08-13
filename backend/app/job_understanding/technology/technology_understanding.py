"""
app.job_understanding.technology.technology_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines required technologies.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


class TechnologyUnderstanding:

    def analyze(
        self,
        job: JobDescriptionModel,
        understanding: JobUnderstanding,
    ) -> JobUnderstanding:

        understanding.required_technologies = sorted(
            technology.name
            for technology in job.technologies.values()
        )

        return understanding