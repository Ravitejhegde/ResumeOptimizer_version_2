from __future__ import annotations

from app.engine.models.document import Document


class ATSAnalyzer:
    """
    Performs ATS-related structural analysis.

    This analyzer evaluates only measurable ATS
    characteristics. It never modifies the document.
    """

    REQUIRED_SECTIONS = {

        "summary",

        "experience",

        "skills",

        "education",

    }

    def analyze(
        self,
        document: Document,
    ) -> dict:

        section_names = {

            paragraph.section

            for paragraph in document.paragraphs

            if paragraph.section

        }

        missing_sections = sorted(

            self.REQUIRED_SECTIONS
            -
            section_names

        )

        has_tables = len(
            document.tables
        ) > 0

        paragraph_count = len(
            document.paragraphs
        )

        empty_paragraphs = sum(

            1

            for paragraph in document.paragraphs

            if not paragraph.text.strip()

        )

        score = 100

        score -= len(
            missing_sections
        ) * 8

        if has_tables:

            score -= 5

        if empty_paragraphs > 5:

            score -= 3

        score = max(
            0,
            min(score, 100),
        )

        return {

            "ats_score": score,

            "required_sections": sorted(
                self.REQUIRED_SECTIONS
            ),

            "missing_sections": missing_sections,

            "has_tables": has_tables,

            "paragraph_count": paragraph_count,

            "empty_paragraphs": empty_paragraphs,

            "is_ats_friendly": score >= 80,

        }