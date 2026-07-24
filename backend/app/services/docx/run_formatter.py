from docx.shared import Pt, RGBColor


class RunFormatter:

    @staticmethod
    def restore(
        run,
        snapshot,
    ):

        # -----------------------------------------
        # Character Formatting
        # -----------------------------------------

        run.bold = snapshot.bold
        run.italic = snapshot.italic
        run.underline = snapshot.underline

        run.font.strike = snapshot.strike
        run.font.superscript = snapshot.superscript
        run.font.subscript = snapshot.subscript
        run.font.all_caps = snapshot.all_caps
        run.font.small_caps = snapshot.small_caps
        run.font.hidden = snapshot.hidden

        # -----------------------------------------
        # Font
        # -----------------------------------------

        if snapshot.font_name:
            run.font.name = snapshot.font_name

        if snapshot.font_size:
            run.font.size = Pt(
                snapshot.font_size
            )

        # -----------------------------------------
        # Color
        # -----------------------------------------

        if snapshot.color:

            try:

                run.font.color.rgb = RGBColor.from_string(
                    snapshot.color
                )

            except Exception:

                pass