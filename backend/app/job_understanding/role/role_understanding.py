"""
app.job_understanding.role.role_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the primary role of a Job Description.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


class RoleUnderstanding:
    """
    Determines role understanding.
    """

    def analyze(
        self,
        job: JobDescriptionModel,
        understanding: JobUnderstanding,
    ) -> JobUnderstanding:

        if not job.roles:
            return understanding

        roles = sorted(
            job.roles.values(),
            key=lambda role: role.confidence,
            reverse=True,
        )

        understanding.target_role = roles[0].name

        return understanding