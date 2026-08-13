"""
app.understanding.experience.experience_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the strongest work experience.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class ExperienceUnderstanding:
    """
    Determines experience-related understanding.
    """

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        if not document.experiences:
            return understanding

        # MVP:
        # Assume the first parsed experience is the strongest.
        strongest = document.experiences[0]

        understanding.strongest_experience = (
            strongest.title
        )

        return understanding