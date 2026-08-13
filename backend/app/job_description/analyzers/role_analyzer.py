"""
app.job_description.analyzers.role_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detects candidate roles from a Job Description.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.analyzer.models.role_model import (
    RoleModel,
)
from app.knowledge.provider import (
    get_knowledge,
)


class RoleAnalyzer:
    """
    Detects roles mentioned in the Job Description.
    """

    def __init__(self) -> None:
        self._roles = get_knowledge().roles

    def analyze(
        self,
        job: JobDescriptionModel,
    ) -> JobDescriptionModel:
        """
        Populate job.roles.
        """

        text = job.text.lower()

        job.roles.clear()

        for role in self._roles.all():

            name = role["name"].lower()

            if name in text:

                model = RoleModel(
                    id=role["id"],
                    name=role["name"],
                    confidence=1.0,
                )

                job.roles[model.id] = model

        return job