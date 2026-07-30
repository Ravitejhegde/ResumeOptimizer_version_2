from __future__ import annotations

import math

from app.engine.models.document.layout_budget import (
    LayoutBudget,
)
from app.engine.models.document.page_geometry import (
    PageGeometry,
)
from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.reader.paragraph_geometry_reader import (
    ParagraphGeometryReader,
)


class LayoutBudgetReader:
    """
    Builds layout constraints for a paragraph.

    Responsibilities:
        - Calculate original content size.
        - Estimate available space.
        - Create layout budget.
        - Preserve original formatting constraints.

    This reader NEVER modifies the document.
    """

    DEFAULT_CHARACTER_WIDTH = 5.5

    @staticmethod
    def build(
        paragraph: Paragraph,
        page_geometry: PageGeometry,
        page_number: int = 1,
    ) -> LayoutBudget:

        text = paragraph.text or ""

        words = text.split()

        characters = len(text)

        estimated_lines = (
            LayoutBudgetReader._estimate_lines(
                paragraph=paragraph,
                page_geometry=page_geometry,
            )
        )

        paragraph_geometry = (
            ParagraphGeometryReader.build(
                paragraph=paragraph,
                page=page_geometry,
                page_number=page_number,
            )
        )

        return LayoutBudget(

            # ----------------------------------
            # Original content
            # ----------------------------------

            original_characters=characters,

            original_words=len(words),

            original_lines=estimated_lines,


            # ----------------------------------
            # Allowed budget
            # ----------------------------------

            max_characters=characters,

            max_words=len(words),

            max_lines=estimated_lines,


            # ----------------------------------
            # Page information
            # ----------------------------------

            page_number=page_number,

            page_geometry=page_geometry,


            # ----------------------------------
            # Paragraph geometry
            # ----------------------------------

            paragraph_geometry=paragraph_geometry,


            # ----------------------------------
            # Formatting constraints
            # ----------------------------------

            left_indent=paragraph.left_indent,

            right_indent=paragraph.right_indent,

            first_line_indent=paragraph.first_line_indent,

            line_spacing=paragraph.line_spacing,

            space_before=paragraph.space_before,

            space_after=paragraph.space_after,


            # ----------------------------------
            # Validation rules
            # ----------------------------------

            allow_overflow=False,

            tolerance_percentage=5.0,
        )


    @staticmethod
    def _estimate_lines(
        paragraph: Paragraph,
        page_geometry: PageGeometry,
    ) -> int:
        """
        Estimate rendered line count.

        Uses printable width instead of only
        newline characters.
        """

        text = paragraph.text.strip()

        if not text:
            return 1


        printable_width = (
            page_geometry.printable_width
        )


        # approximate characters per line

        chars_per_line = max(
            1,
            int(
                printable_width
                /
                LayoutBudgetReader.DEFAULT_CHARACTER_WIDTH
            ),
        )


        estimated = math.ceil(
            len(text)
            /
            chars_per_line
        )


        return max(
            1,
            estimated,
        )