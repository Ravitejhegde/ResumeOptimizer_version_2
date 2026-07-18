from docx.shared import Pt


class ParagraphFormatter:

    @staticmethod
    def restore(
        paragraph,
        paragraph_format,
    ):

        if paragraph_format is None:
            return

        pf = paragraph.paragraph_format

        pf.alignment = paragraph_format.alignment

        if paragraph_format.left_indent is not None:
            pf.left_indent = Pt(
                paragraph_format.left_indent
            )

        if paragraph_format.right_indent is not None:
            pf.right_indent = Pt(
                paragraph_format.right_indent
            )

        if paragraph_format.first_line_indent is not None:
            pf.first_line_indent = Pt(
                paragraph_format.first_line_indent
            )

        if paragraph_format.space_before is not None:
            pf.space_before = Pt(
                paragraph_format.space_before
            )

        if paragraph_format.space_after is not None:
            pf.space_after = Pt(
                paragraph_format.space_after
            )

        if paragraph_format.line_spacing is not None:
            pf.line_spacing = (
                paragraph_format.line_spacing
            )

        pf.keep_together = (
            paragraph_format.keep_together
        )

        pf.keep_with_next = (
            paragraph_format.keep_with_next
        )

        pf.page_break_before = (
            paragraph_format.page_break_before
        )