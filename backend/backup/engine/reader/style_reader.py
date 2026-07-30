from __future__ import annotations

from docx.text.run import Run as DocxRun
from docx.shared import RGBColor

from app.engine.models.document.text_style import (
    TextStyle,
)


class StyleReader:
    """
    Reads character formatting from a python-docx Run.

    Responsibilities:
        - Convert Word font formatting
        - Preserve character style information
        - Create immutable TextStyle model

    Does not:
        - Modify DOCX
        - Apply styles
        - Optimize content
    """


    @staticmethod
    def read(
        docx_run: DocxRun,
    ) -> TextStyle:
        """
        Convert python-docx Run formatting
        into engine TextStyle.
        """

        if docx_run is None:
            raise ValueError(
                "DOCX run cannot be None."
            )


        font = docx_run.font


        return TextStyle(

            # ----------------------------------
            # Font
            # ----------------------------------

            font_name=(
                font.name
            ),

            font_size=(
                font.size.pt
                if font.size
                else None
            ),


            # ----------------------------------
            # Basic formatting
            # ----------------------------------

            bold=(
                bool(docx_run.bold)
            ),

            italic=(
                bool(docx_run.italic)
            ),

            underline=(
                bool(docx_run.underline)
            ),

            strike=(
                bool(font.strike)
            ),


            # ----------------------------------
            # Typography
            # ----------------------------------

            subscript=(
                bool(font.subscript)
            ),

            superscript=(
                bool(font.superscript)
            ),

            small_caps=(
                bool(font.small_caps)
            ),

            all_caps=(
                bool(font.all_caps)
            ),


            # ----------------------------------
            # Colors
            # ----------------------------------

            color=(
                StyleReader._read_color(
                    font.color.rgb
                    if font.color
                    else None
                )
            ),


            highlight=(
                str(font.highlight_color)
                if font.highlight_color
                else None
            ),


            # ----------------------------------
            # Visibility
            # ----------------------------------

            hidden=(
                bool(font.hidden)
            ),
        )


    @staticmethod
    def _read_color(
        color,
    ) -> str | None:
        """
        Extract RGB color safely.
        """

        if isinstance(
            color,
            RGBColor,
        ):
            return str(color)


        return None