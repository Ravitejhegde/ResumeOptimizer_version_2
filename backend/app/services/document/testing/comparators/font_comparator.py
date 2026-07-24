from docx import Document

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class FontComparator:
    """
    Compares fonts used throughout the document.
    """

    @classmethod
    def compare(
        cls,
        original: Document,
        optimized: Document,
        result: ComparisonResult,
    ):

        original_fonts = cls._collect_fonts(original)
        optimized_fonts = cls._collect_fonts(optimized)

        result.add(
            "Document Fonts",
            sorted(original_fonts),
            sorted(optimized_fonts),
        )

    @classmethod
    def _collect_fonts(cls, document):

        fonts = set()

        for paragraph in document.paragraphs:

            for run in paragraph.runs:

                if run.font.name:
                    fonts.add(run.font.name)

        return fonts