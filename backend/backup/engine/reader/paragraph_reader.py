from __future__ import annotations

from docx.text.paragraph import (
    Paragraph as DocxParagraph,
)

from app.engine.models.document.page_geometry import (
    PageGeometry,
)
from app.engine.models.document.paragraph import (
    Paragraph,
)
from app.engine.reader.layout_budget_reader import (
    LayoutBudgetReader,
)
from app.engine.reader.numbering_reader import (
    NumberingReader,
)
from app.engine.reader.run_reader import (
    RunReader,
)


class ParagraphReader:
    """
    Reads a Word paragraph into the engine model.

    Responsibilities:
        - Extract runs
        - Extract formatting
        - Extract numbering
        - Build layout budget

    Does not:
        - Modify DOCX
        - Optimize text
    """

    @staticmethod
    def read(
        docx_paragraph: DocxParagraph,
        paragraph_id: str,
        page_geometry: PageGeometry,
        page_number: int = 1,
    ) -> Paragraph:

        runs = [
            RunReader.read(run)
            for run in docx_paragraph.runs
        ]


        paragraph_format = (
            docx_paragraph.paragraph_format
        )


        paragraph = Paragraph(

            id=paragraph_id,

            runs=runs,


            # ----------------------------------
            # Style
            # ----------------------------------

            style_name=(
                docx_paragraph.style.name
                if docx_paragraph.style
                else "Normal"
            ),


            # ----------------------------------
            # Formatting
            # ----------------------------------

            alignment=(
                str(docx_paragraph.alignment)
                if docx_paragraph.alignment
                else None
            ),


            left_indent=(
                paragraph_format.left_indent.pt
                if paragraph_format.left_indent
                else None
            ),


            right_indent=(
                paragraph_format.right_indent.pt
                if paragraph_format.right_indent
                else None
            ),


            first_line_indent=(
                paragraph_format.first_line_indent.pt
                if paragraph_format.first_line_indent
                else None
            ),


            space_before=(
                paragraph_format.space_before.pt
                if paragraph_format.space_before
                else None
            ),


            space_after=(
                paragraph_format.space_after.pt
                if paragraph_format.space_after
                else None
            ),


            line_spacing=(
                float(
                    paragraph_format.line_spacing
                )
                if paragraph_format.line_spacing
                else None
            ),


            keep_together=bool(
                paragraph_format.keep_together
            ),


            keep_with_next=bool(
                paragraph_format.keep_with_next
            ),


            page_break_before=bool(
                paragraph_format.page_break_before
            ),


            # ----------------------------------
            # Numbering
            # ----------------------------------

            numbering=(
                NumberingReader.read(
                    docx_paragraph
                )
            ),


            editable=True,

            section=None,
        )


        paragraph.layout_budget = (
            LayoutBudgetReader.build(
                paragraph=paragraph,
                page_geometry=page_geometry,
                page_number=page_number,
            )
        )


        return paragraph