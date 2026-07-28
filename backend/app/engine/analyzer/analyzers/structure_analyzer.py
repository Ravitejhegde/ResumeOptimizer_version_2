from __future__ import annotations

from collections import Counter

from app.engine.common.enums import (
    SectionType,
)
from app.engine.models.analysis.structure_analysis import (
    StructureAnalysis,
)
from app.engine.models.document.document import (
    Document,
)


class StructureAnalyzer:
    """
    Analyzes the structure of a resume.

    Responsible only for understanding
    document organization.
    """

    # --------------------------------------------------

    def analyze(
        self,
        document: Document,
    ) -> StructureAnalysis:

        section_counter = Counter()

        run_count = 0

        empty_paragraphs = 0

        for paragraph in document.paragraphs:

            if paragraph.is_empty:

                empty_paragraphs += 1

            run_count += paragraph.run_count

            if paragraph.section:

                section_counter[
                    paragraph.section
                ] += 1

        sections = [

            section.value

            for section in SectionType

            if section.value in section_counter

        ]

        return StructureAnalysis(

            paragraph_count=document.paragraph_count,

            run_count=run_count,

            table_count=document.table_count,

            section_count=len(
                section_counter,
            ),

            empty_paragraphs=empty_paragraphs,

            sections=sections,

            section_distribution=dict(
                section_counter,
            ),

        )
