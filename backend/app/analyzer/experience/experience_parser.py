"""
app.analyzer.experience.experience_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses the Experience section into ExperienceModel objects.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.experience_model import (
    ExperienceModel,
)


class ExperienceParser:
    """
    Parses work experience entries.
    """

    def parse(
        self,
        document: DocumentModel,
    ) -> list[ExperienceModel]:
        """
        Parse work experience from the document.
        """

        experiences: list[ExperienceModel] = []

        section = document.sections.get(
            "experience"
        )

        if section is None:
            return experiences

        paragraphs = [
            p.strip()
            for p in section.paragraphs
            if p.strip()
        ]

        experience = ExperienceModel()

        if len(paragraphs) >= 1:
            experience.title = paragraphs[0]

        if len(paragraphs) >= 2:
            experience.company = paragraphs[1]

        if len(paragraphs) >= 3:
            experience.duration = paragraphs[2]

        if len(paragraphs) > 3:
            experience.description = paragraphs[3:]

        experiences.append(experience)

        return experiences