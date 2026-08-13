"""
app.understanding.technology.technology_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the primary technologies of a resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class TechnologyUnderstanding:
    """
    Determines technology-related understanding.
    """

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        technologies = sorted(
            (
                technology.name
                for technology in document.technologies.values()
            ),
        )

        understanding.primary_technologies = technologies

        return understanding