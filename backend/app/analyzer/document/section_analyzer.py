"""
app.analyzer.document.section_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detects logical sections in a parsed resume.
"""

from __future__ import annotations

from app.analyzer.contracts.section_analyzer_contract import (
    SectionAnalyzerContract,
)
from app.analyzer.document.section_headings import (
    SECTION_HEADINGS,
)
from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.section_model import (
    SectionModel,
)


class SectionAnalyzer(SectionAnalyzerContract):
    """
    Detect logical resume sections.
    """

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:

        sections: dict[str, SectionModel] = {}

        current_section = "document"

        sections[current_section] = SectionModel(
            name=current_section
        )

        for paragraph_index, paragraph in enumerate(
    document.paragraphs
):

            normalized = paragraph.strip().casefold()

            detected = self._detect_heading(
                normalized
            )

            if detected is not None:

                current_section = detected

                sections.setdefault(
                    current_section,
                    SectionModel(
                        name=current_section,
                    ),
                )

                continue

            sections[current_section].paragraph_indexes.append(
    paragraph_index
)

        document.sections = sections

        return document

    def _detect_heading(
        self,
        text: str,
    ) -> str | None:

        for section_name, headings in SECTION_HEADINGS.items():

            if text in headings:
                return section_name

        return None