from docx.text.paragraph import Paragraph
from docx.shared import Pt, RGBColor

from app.services.document.models.run_model import (
    RunModel,
)


class RunWriter:
    """
    Writes RunModel objects back to DOCX.
    """

    @classmethod
    def write(
        cls,
        paragraph: Paragraph,
        runs: list[RunModel],
    ) -> None:

        for run_model in runs:

            run = paragraph.add_run(
                run_model.text
            )

            font = run.font

            # -----------------------------------------
            # Font
            # -----------------------------------------

            font.name = run_model.font_name

            if run_model.font_size:

                font.size = Pt(
                    run_model.font_size
                )

            # -----------------------------------------
            # Character Formatting
            # -----------------------------------------

            font.bold = run_model.bold

            font.italic = run_model.italic

            font.underline = run_model.underline

            font.strike = run_model.strike

            font.double_strike = (
                run_model.double_strike
            )

            font.superscript = (
                run_model.superscript
            )

            font.subscript = (
                run_model.subscript
            )

            font.all_caps = (
                run_model.all_caps
            )

            font.small_caps = (
                run_model.small_caps
            )

            font.hidden = (
                run_model.hidden
            )

            font.outline = (
                run_model.outline
            )

            font.shadow = (
                run_model.shadow
            )

            font.emboss = (
                run_model.emboss
            )

            font.imprint = (
                run_model.engrave
            )

            # -----------------------------------------
            # Color
            # -----------------------------------------

            if run_model.color:

                try:

                    color = run_model.color.replace(
                        "#",
                        "",
                    )

                    if len(color) == 6:

                        font.color.rgb = RGBColor.from_string(
                            color
                        )

                except Exception:

                    pass

            # -----------------------------------------
            # Style
            # -----------------------------------------

            try:

                if run_model.style:

                    run.style = run_model.style

            except Exception:

                pass