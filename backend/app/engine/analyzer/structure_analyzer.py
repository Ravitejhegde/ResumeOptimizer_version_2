from __future__ import annotations

from collections import Counter

from app.engine.common.enums import SectionType
from app.engine.models.document import Document


class StructureAnalyzer:
    """
    Analyzes the structural organization of a resume.

    Responsible ONLY for understanding document
    structure.

    Never modifies the document.
    """

    def analyze(
        self,
        document: Document,
    ) -> dict:

        section_counter = Counter()

        empty_paragraphs = 0

        total_runs = 0

        total_tables = len(
            document.tables
        )

        for paragraph in document.paragraphs:

            if not paragraph.text.strip():

                empty_paragraphs += 1

            total_runs += len(
                paragraph.runs
            )

            if paragraph.section:

                section_counter[
                    paragraph.section
                ] += 1

        detected_sections = [

            section

            for section in SectionType

            if section.value in section_counter

        ]

        return {

            "paragraphs": len(
                document.paragraphs
            ),

            "runs": total_runs,

            "tables": total_tables,

            "empty_paragraphs": empty_paragraphs,

            "sections": detected_sections,

            "section_distribution": dict(
                section_counter
            ),

        }