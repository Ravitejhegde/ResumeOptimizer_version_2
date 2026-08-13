"""
app.analyzer.experience.experience_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extracts professional experience from a resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.experience.experience_parser import (
    ExperienceParser,
)


class ExperienceAnalyzer:
    """
    Populates document.experiences.
    """

    def __init__(self) -> None:
        self._parser = ExperienceParser()

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Extract work experience entries.
        """

        document.experiences = (
            self._parser.parse(
                document
            )
        )

        return document