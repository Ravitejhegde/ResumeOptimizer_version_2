"""
app.job_description.analyzers.technology_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detects technologies mentioned in a Job Description.
"""

from __future__ import annotations

from app.analyzer.models.technology_model import (
    TechnologyModel,
)
from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.knowledge.provider import (
    get_knowledge,
)


class TechnologyAnalyzer:
    """
    Detects technologies from a Job Description.
    """

    def __init__(self) -> None:
        self._technologies = (
            get_knowledge().technologies
        )

    def analyze(
        self,
        job: JobDescriptionModel,
    ) -> JobDescriptionModel:
        """
        Populate job.technologies.
        """

        text = job.text.lower()

        job.technologies.clear()

        for technology in self._technologies.all():

            name = technology["name"].lower()

            if name in text:

                model = TechnologyModel(
                    id=technology["id"],
                    name=technology["name"],
                    confidence=1.0,
                )

                job.technologies[
                    model.id
                ] = model

        return job