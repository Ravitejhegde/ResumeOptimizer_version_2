from docx.text.run import Run

from app.services.document.models.run_model import (
    RunModel,
)


class RunParser:
    """
    Parses Word runs into RunModel.
    """

    @classmethod
    def parse(
        cls,
        runs: list[Run],
    ) -> list[RunModel]:

        result = []

        for run in runs:

            model = RunModel()

            # -----------------------------------------
            # Text
            # -----------------------------------------

            model.text = run.text

            # -----------------------------------------
            # Font
            # -----------------------------------------

            font = run.font

            model.font_name = font.name or ""

            model.font_size = (
                font.size.pt
                if font.size
                else 0
            )

            # -----------------------------------------
            # Character Formatting
            # -----------------------------------------

            model.bold = bool(font.bold)

            model.italic = bool(font.italic)

            model.underline = bool(font.underline)

            model.strike = bool(font.strike)

            model.double_strike = bool(
                font.double_strike
            )

            model.superscript = bool(
                font.superscript
            )

            model.subscript = bool(
                font.subscript
            )

            model.all_caps = bool(
                font.all_caps
            )

            model.small_caps = bool(
                font.small_caps
            )

            model.hidden = bool(
                font.hidden
            )

            model.outline = bool(
                font.outline
            )

            model.shadow = bool(
                font.shadow
            )

            model.emboss = bool(
                font.emboss
            )

            model.engrave = bool(
                font.imprint
            )

            # -----------------------------------------
            # Colors
            # -----------------------------------------

            if font.color:

                model.color = str(
                    font.color.rgb
                )

                model.theme_color = str(
                    font.color.theme_color
                )

            model.highlight = str(
                font.highlight_color
            )

            # -----------------------------------------
            # Style
            # -----------------------------------------

            if run.style:

                model.style = run.style.name

            result.append(model)

        return result