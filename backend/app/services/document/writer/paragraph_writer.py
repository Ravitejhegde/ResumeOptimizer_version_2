from docx.document import Document as DocxDocument
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from app.services.document.models.paragraph_model import (
    ParagraphModel,
)

from app.services.document.writer.run_writer import (
    RunWriter,
)


class ParagraphWriter:
    """
    Writes ParagraphModel objects to DOCX.
    """

    ALIGNMENTS = {
        "LEFT": WD_ALIGN_PARAGRAPH.LEFT,
        "CENTER": WD_ALIGN_PARAGRAPH.CENTER,
        "RIGHT": WD_ALIGN_PARAGRAPH.RIGHT,
        "JUSTIFY": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }

    @classmethod
    def write(
        cls,
        document: DocxDocument,
        paragraphs: list[ParagraphModel],
    ) -> None:

        for paragraph_model in paragraphs:

            paragraph = document.add_paragraph()

            # -----------------------------------------
            # Style
            # -----------------------------------------

            try:

                if paragraph_model.style:

                    paragraph.style = paragraph_model.style

            except Exception:

                pass

            # -----------------------------------------
            # Alignment
            # -----------------------------------------

            alignment = cls.ALIGNMENTS.get(
                paragraph_model.alignment.upper()
            )

            if alignment is not None:

                paragraph.alignment = alignment

            # -----------------------------------------
            # Paragraph Formatting
            # -----------------------------------------

            fmt = paragraph.paragraph_format

            fmt.left_indent = Pt(
                paragraph_model.left_indent
            )

            fmt.right_indent = Pt(
                paragraph_model.right_indent
            )

            fmt.first_line_indent = Pt(
                paragraph_model.first_line_indent
            )

            fmt.space_before = Pt(
                paragraph_model.spacing_before
            )

            fmt.space_after = Pt(
                paragraph_model.spacing_after
            )

            fmt.keep_together = (
                paragraph_model.keep_together
            )

            fmt.keep_with_next = (
                paragraph_model.keep_with_next
            )

            fmt.page_break_before = (
                paragraph_model.page_break_before
            )

            fmt.widow_control = (
                paragraph_model.widow_control
            )

            # -----------------------------------------
            # Runs
            # -----------------------------------------

            RunWriter.write(
                paragraph,
                paragraph_model.runs,
            )