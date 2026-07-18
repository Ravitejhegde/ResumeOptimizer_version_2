class RunFormatter:

    @staticmethod
    def restore(
        run,
        snapshot,
    ):

        run.bold = snapshot.bold

        run.italic = snapshot.italic

        run.underline = snapshot.underline

        if snapshot.font_name:
            run.font.name = snapshot.font_name

        if snapshot.font_size:
            from docx.shared import Pt

            run.font.size = Pt(
                snapshot.font_size
            )

        if snapshot.color:
            from docx.shared import RGBColor

            try:

                run.font.color.rgb = RGBColor.from_string(
                    snapshot.color
                )

            except Exception:

                pass