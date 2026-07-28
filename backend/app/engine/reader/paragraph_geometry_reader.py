from __future__ import annotations

from app.engine.models.document.page_geometry import (
    PageGeometry,
)

from app.engine.models.document.paragraph import Paragraph

from app.engine.models.document.paragraph_geometry import (
    ParagraphGeometry,
)


class ParagraphGeometryReader:
    """
    Calculates paragraph geometry.

    This class estimates the rendering space
    occupied by a paragraph.

    Future versions will use font metrics and
    actual rendering measurements.
    """

    @staticmethod
    def build(
        paragraph: Paragraph,
        page: PageGeometry,
        page_number: int = 1,
    ) -> ParagraphGeometry:

        text = paragraph.text

        printable_width = page.printable_width

        # ----------------------------------------
        # Initial estimation
        # ----------------------------------------

        estimated_lines = max(
            1,
            text.count("\n") + 1,
        )

        estimated_height = (

            estimated_lines

            * (

                paragraph.line_spacing

                if paragraph.line_spacing

                else 12

            )

        )

        return ParagraphGeometry(

            page_number=page_number,

            available_width=printable_width,

            available_height=page.printable_height,

            x=None,

            y=None,

            estimated_width=printable_width,

            estimated_height=estimated_height,

            estimated_line_count=estimated_lines,

            may_overflow=False,

        )




