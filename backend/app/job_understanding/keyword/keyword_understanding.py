"""
app.job_understanding.keyword.keyword_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines important keywords.
"""

from __future__ import annotations

from app.job_description.models.job_description_model import (
    JobDescriptionModel,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


class KeywordUnderstanding:
    """
    MVP keyword understanding.
    """

    def analyze(
        self,
        job: JobDescriptionModel,
        understanding: JobUnderstanding,
    ) -> JobUnderstanding:

        understanding.required_keywords = []

        return understanding