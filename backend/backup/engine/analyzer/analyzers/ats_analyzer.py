from __future__ import annotations

from app.engine.models.analysis.ats_analysis import (
    ATSAnalysis,
)
from app.engine.models.document.document import (
    Document,
)


class ATSAnalyzer:
    """
    Performs ATS compatibility analysis.

    Responsible only for measuring ATS
    friendliness. Never modifies the document.
    """

    REQUIRED_SECTIONS = {
        "summary",
        "experience",
        "skills",
        "education",
    }

    SECTION_PENALTY = 8
    TABLE_PENALTY = 5
    EMPTY_PARAGRAPH_PENALTY = 3

    # --------------------------------------------------

    def analyze(
        self,
        document: Document,
    ) -> ATSAnalysis:

        sections = {

            paragraph.section.lower()

            for paragraph in document.paragraphs

            if paragraph.section

        }

        missing = sorted(

            self.REQUIRED_SECTIONS
            - sections

        )

        score = self._calculate_score(

            missing_sections=missing,

            has_tables=(
                document.table_count > 0
            ),

            empty_paragraphs=sum(

                1

                for paragraph
                in document.paragraphs

                if paragraph.is_empty

            ),

        )

        return ATSAnalysis(

            score=score,

            is_ats_friendly=(
                score >= 80
            ),

            required_sections=sorted(
                self.REQUIRED_SECTIONS,
            ),

            missing_sections=missing,

            paragraph_count=document.paragraph_count,

            empty_paragraphs=sum(

                1

                for paragraph
                in document.paragraphs

                if paragraph.is_empty

            ),

            has_tables=(
                document.table_count > 0
            ),

            warnings=[],

        )

    # --------------------------------------------------

    def _calculate_score(
        self,
        missing_sections: list[str],
        has_tables: bool,
        empty_paragraphs: int,
    ) -> int:

        score = 100

        score -= (
            len(missing_sections)
            * self.SECTION_PENALTY
        )

        if has_tables:

            score -= self.TABLE_PENALTY

        if empty_paragraphs > 5:

            score -= (
                self.EMPTY_PARAGRAPH_PENALTY
            )

        return max(
            0,
            min(
                score,
                100,
            ),
        )
