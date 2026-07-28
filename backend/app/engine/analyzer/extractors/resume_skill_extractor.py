from __future__ import annotations

from app.engine.models.document.document import Document
from app.engine.analyzer.extractors.technology_extractor import (
    TechnologyExtractor,
)


class ResumeSkillExtractor:
    """
    Extract technologies from a parsed resume.
    """

    def __init__(
        self,
        extractor: TechnologyExtractor,
    ) -> None:

        self._extractor = extractor

    # --------------------------------------------------

    def extract(
        self,
        document: Document,
    ) -> list[str]:

        detected: set[str] = set()

        for paragraph in document.paragraphs:

            if not paragraph.text.strip():
                continue

            detected.update(

                self._extractor.extract(
                    paragraph.text,
                )

            )

        return sorted(
            detected,
        )
