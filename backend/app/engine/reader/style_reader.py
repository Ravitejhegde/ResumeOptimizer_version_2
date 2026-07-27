from __future__ import annotations

from docx.text.run import Run as DocxRun
from docx.shared import RGBColor

from app.engine.models.text_style import TextStyle


class StyleReader:
    """
    Reads character formatting from a python-docx Run.

    This class is responsible ONLY for converting
    Word formatting into the engine TextStyle model.
    """

    @staticmethod
    def read(
        docx_run: DocxRun,
    ) -> TextStyle:

        font = docx_run.font

        color = None

        if (
            font.color is not None
            and isinstance(font.color.rgb, RGBColor)
        ):
            color = str(font.color.rgb)

        return TextStyle(

            font_name=font.name,

            font_size=(
                font.size.pt
                if font.size
                else None
            ),

            bold=bool(docx_run.bold),

            italic=bool(docx_run.italic),

            underline=bool(docx_run.underline),

            strike=bool(font.strike),

            subscript=bool(font.subscript),

            superscript=bool(font.superscript),

            small_caps=bool(font.small_caps),

            all_caps=bool(font.all_caps),

            hidden=bool(font.hidden),

            color=color,

            highlight=(
                str(font.highlight_color)
                if font.highlight_color
                else None
            ),
        )




