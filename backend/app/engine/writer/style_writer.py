from __future__ import annotations

from docx.text.run import Run


class StyleWriter:
    """
    Copies formatting from one DOCX run
    to another.

    Responsibilities
    ----------------
    • Preserve character formatting
    • Never modify text
    • Never modify paragraph layout
    • Never create/delete runs
    """

    @staticmethod
    def apply(
        source: Run,
        target: Run,
    ) -> None:
        """
        Copy formatting from the original run
        to the rewritten run.
        """

        StyleWriter._copy_style(
            source,
            target,
        )

        StyleWriter._copy_font(
            source,
            target,
        )

    # --------------------------------------------------

    @staticmethod
    def _copy_style(
        source: Run,
        target: Run,
    ) -> None:

        target.style = source.style

    # --------------------------------------------------

    @staticmethod
    def _copy_font(
        source: Run,
        target: Run,
    ) -> None:

        src = source.font
        dst = target.font

        dst.name = src.name
        dst.size = src.size

        dst.bold = src.bold
        dst.italic = src.italic
        dst.underline = src.underline

        dst.strike = src.strike
        dst.double_strike = src.double_strike

        dst.subscript = src.subscript
        dst.superscript = src.superscript

        dst.small_caps = src.small_caps
        dst.all_caps = src.all_caps

        dst.hidden = src.hidden

        dst.shadow = src.shadow
        dst.outline = src.outline

        dst.emboss = src.emboss
        dst.imprint = src.imprint

        dst.highlight_color = (
            src.highlight_color
        )

        if src.color is not None:

            dst.color.rgb = src.color.rgb

            dst.color.theme_color = (
                src.color.theme_color
            )

            dst.color.type = (
                src.color.type
            )

        dst.complex_script = (
            src.complex_script
        )

        dst.cs_bold = src.cs_bold
        dst.cs_italic = src.cs_italic

        dst.math = src.math

        dst.no_proof = src.no_proof

        dst.rtl = src.rtl

        dst.snap_to_grid = (
            src.snap_to_grid
        )

        dst.spec_vanish = (
            src.spec_vanish
        )

        dst.web_hidden = (
            src.web_hidden
        )