from docx import Document

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class ImageComparator:
    """
    Compares embedded images.
    """

    @classmethod
    def compare(
        cls,
        original: Document,
        optimized: Document,
        result: ComparisonResult,
    ):

        result.add(
            "Inline Images",
            len(original.inline_shapes),
            len(optimized.inline_shapes),
        )