from __future__ import annotations

from docx.section import Section

from app.engine.models.document.page_geometry import (
    PageGeometry,
)


class PageGeometryReader:
    """
    Reads physical page geometry from a DOCX section.

    Responsibilities:
        - Extract page size.
        - Extract margins.
        - Extract header/footer spacing.
        - Preserve layout information.

    This reader does not modify the document.
    """

    @staticmethod
    def read(
        section: Section,
    ) -> PageGeometry:
        """
        Convert Word section geometry into
        engine PageGeometry model.
        """

        return PageGeometry(

            # ----------------------------------
            # Page size
            # ----------------------------------

            width=(
                section.page_width.pt
                if section.page_width
                else 0
            ),

            height=(
                section.page_height.pt
                if section.page_height
                else 0
            ),


            # ----------------------------------
            # Margins
            # ----------------------------------

            margin_left=(
                section.left_margin.pt
                if section.left_margin
                else 0
            ),

            margin_right=(
                section.right_margin.pt
                if section.right_margin
                else 0
            ),

            margin_top=(
                section.top_margin.pt
                if section.top_margin
                else 0
            ),

            margin_bottom=(
                section.bottom_margin.pt
                if section.bottom_margin
                else 0
            ),


            # ----------------------------------
            # Header / Footer
            # ----------------------------------

            header_distance=(
                section.header_distance.pt
                if section.header_distance
                else 0
            ),

            footer_distance=(
                section.footer_distance.pt
                if section.footer_distance
                else 0
            ),


            # ----------------------------------
            # Binding
            # ----------------------------------

            gutter=(
                section.gutter.pt
                if section.gutter
                else 0
            ),


            # ----------------------------------
            # Columns
            # ----------------------------------

            columns=(
                PageGeometryReader._read_columns(
                    section
                )
            ),
        )


    @staticmethod
    def _read_columns(
        section: Section,
    ) -> int:
        """
        Reads document column count.

        python-docx does not expose columns
        directly, so XML inspection is required.
        """

        try:

            sect_pr = section._sectPr

            cols = sect_pr.cols

            if cols is not None and cols.num:

                return int(
                    cols.num
                )

        except Exception:

            pass

        return 1