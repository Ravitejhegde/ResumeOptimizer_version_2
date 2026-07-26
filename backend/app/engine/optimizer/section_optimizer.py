from __future__ import annotations

from dataclasses import replace

from app.engine.models.paragraph import Paragraph
from app.engine.common.enums import SectionType


class SectionOptimizer:
    """
    Applies section-level optimizations.

    Responsibilities
    ----------------
    - Rename section headings
    - Preserve paragraph formatting
    - Preserve layout
    - Preserve hyperlinks
    - Never modify locked sections

    This class NEVER calls AI.
    """

    @staticmethod
    def rename(
        paragraph: Paragraph,
        new_heading: str,
    ) -> Paragraph:

        if not paragraph.editable:
            return paragraph

        if paragraph.section in (
            SectionType.EDUCATION.value,
            SectionType.CERTIFICATIONS.value,
        ):
            return paragraph

        optimized = replace(
            paragraph
        )

        if not optimized.runs:
            return optimized

        optimized.runs[0].text = new_heading

        for run in optimized.runs[1:]:

            run.text = ""

        return optimized