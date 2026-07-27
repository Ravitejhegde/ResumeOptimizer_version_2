from __future__ import annotations

from app.engine.models.analysis_result import (
    ATSAnalysisResult,
)
from app.engine.models.document import (
    Document,
)


class ATSAnalyzer:
    """
    Performs ATS structural analysis.

    Evaluates measurable ATS characteristics
    without modifying the document.
    """

    SECTION_PENALTY = 8
    TABLE_PENALTY = 5
    EMPTY_PARAGRAPH_PENALTY = 3

    REQUIRED_SECTIONS = {
        "summary",
        "experience",
        "skills",
        "education",
    }

    def analyze(
        self,
        document: Document,
    ) -> ATSAnalysisResult:

        section_names = {

            paragraph.section.lower()

            for paragraph in document.paragraphs

            if paragraph.section

        }

        missing_sections = sorted(

            self.REQUIRED_SECTIONS
            - section_names

        )

        has_tables = (
            len(document.tables) > 0
        )

        paragraph_count = len(
            document.paragraphs
        )

        empty_paragraphs = sum(

            1

            for paragraph in document.paragraphs

            if not paragraph.text.strip()

        )

        score = self._calculate_score(

            missing_sections,

            has_tables,

            empty_paragraphs,

        )

        return ATSAnalysisResult(

            score=score,

            required_sections=sorted(
                self.REQUIRED_SECTIONS
            ),

            missing_sections=missing_sections,

            has_tables=has_tables,

            paragraph_count=paragraph_count,

            empty_paragraphs=empty_paragraphs,

            is_ats_friendly=(
                score >= 80
            ),

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
            min(score, 100),
        )