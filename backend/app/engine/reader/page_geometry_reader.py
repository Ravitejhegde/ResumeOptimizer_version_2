from __future__ import annotations

from docx.section import Section

from app.engine.models.document.page_geometry import (
    PageGeometry,
)


class PageGeometryReader:
    """
    Reads page geometry from a Word document section.
    """

    @staticmethod
    def read(
        section: Section,
    ) -> PageGeometry:

        return PageGeometry(

            width=section.page_width.pt,

            height=section.page_height.pt,

            margin_left=section.left_margin.pt,

            margin_right=section.right_margin.pt,

            margin_top=section.top_margin.pt,

            margin_bottom=section.bottom_margin.pt,

            header_distance=section.header_distance.pt,

            footer_distance=section.footer_distance.pt,

            gutter=section.gutter.pt,

            columns=1,

        )




