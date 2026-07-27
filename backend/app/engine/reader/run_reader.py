from __future__ import annotations

from docx.text.run import Run as DocxRun
from docx.shared import RGBColor

from app.engine.models.run import Run
from app.engine.models.text_style import TextStyle
from app.engine.common.enums import ObjectType


class RunReader:
    """
    Reads a python-docx Run and converts it into
    the engine Run model.

    This class is responsible ONLY for reading a
    single run.
    """

    @staticmethod
    def read(
        docx_run: DocxRun,
    ) -> Run:
        """
        Convert a python-docx Run into an engine Run.
        """

        font = docx_run.font

        color = None

        if (
            font.color is not None
            and isinstance(font.color.rgb, RGBColor)
        ):
            color = str(font.color.rgb)

        style = TextStyle(

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

        return Run(

            text=docx_run.text,

            style=style,

            hyperlink=None,

            editable=True,

            locked_reason=None,

            object_type=ObjectType.TEXT.value,

        )




