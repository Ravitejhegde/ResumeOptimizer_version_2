from __future__ import annotations

from app.engine.models.layout_budget import LayoutBudget
from app.engine.models.page_geometry import PageGeometry
from app.engine.models.paragraph import Paragraph

from app.engine.reader.paragraph_geometry_reader import (
    ParagraphGeometryReader,
)


class LayoutBudgetReader:
    """
    Calculates the layout budget for a paragraph.

    This class NEVER modifies the document.

    It only measures the available layout space.
    """

    @staticmethod
    def build(
        paragraph: Paragraph,
        page_geometry: PageGeometry,
        page_number: int = 1,
    ) -> LayoutBudget:

        text = paragraph.text

        words = text.split()

        characters = len(text)

        estimated_lines = max(
            1,
            text.count("\n") + 1,
        )

        paragraph_geometry = ParagraphGeometryReader.build(
            paragraph=paragraph,
            page=page_geometry,
            page_number=page_number,
        )

        return LayoutBudget(

            # Original content
            original_characters=characters,
            original_words=len(words),
            original_lines=estimated_lines,

            # Budget
            max_characters=characters,
            max_words=len(words),
            max_lines=estimated_lines,

            # Page
            page_number=page_number,
            page_geometry=page_geometry,

            # Paragraph geometry
            paragraph_geometry=paragraph_geometry,

            # Formatting
            left_indent=paragraph.left_indent,
            right_indent=paragraph.right_indent,
            first_line_indent=paragraph.first_line_indent,
            line_spacing=paragraph.line_spacing,
            space_before=paragraph.space_before,
            space_after=paragraph.space_after,

            # Validation
            allow_overflow=False,
            tolerance_percentage=0.0,
        )




