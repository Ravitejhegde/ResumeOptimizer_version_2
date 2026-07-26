from __future__ import annotations

from docx.section import Section

from app.engine.models.page_geometry import (
    PageGeometry,
)


class PageGeometryReader:
    """
    Reads physical page geometry from a Word section.
    """

    @staticmethod
    def read(
        section: Section,
    ) -> PageGeometry:

        setup = section

        return PageGeometry(

            width=setup.page_width.pt,

            height=setup.page_height.pt,

            margin_left=setup.left_margin.pt,

            margin_right=setup.right_margin.pt,

            margin_top=setup.top_margin.pt,

            margin_bottom=setup.bottom_margin.pt,

            header_distance=setup.header_distance.pt,

            footer_distance=setup.footer_distance.pt,

            gutter=setup.gutter.pt,

            columns=1,

        )