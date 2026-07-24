from docx import Document

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class PageComparator:
    """
    Placeholder.

    python-docx cannot calculate rendered
    page count.
    """

    @classmethod
    def compare(
        cls,
        original: Document,
        optimized: Document,
        result: ComparisonResult,
    ):

        result.add(
            "Sections",
            len(original.sections),
            len(optimized.sections),
        )

        result.add(
            "Paragraphs",
            len(original.paragraphs),
            len(optimized.paragraphs),
        )