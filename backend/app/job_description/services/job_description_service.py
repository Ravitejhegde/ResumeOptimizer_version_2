"""
app.job_description.services.job_description_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for job description parsing.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)

from app.job_description.services.job_description_parser import (
    JobDescriptionParser,
)


class JobDescriptionService:
    """
    Public service for job description parsing.
    """

    def __init__(
        self,
    ) -> None:

        self._parser = JobDescriptionParser()

    def analyze(
        self,
        text: str,
    ) -> JobDescriptionModel:

        return self._parser.parse(
            text
        )