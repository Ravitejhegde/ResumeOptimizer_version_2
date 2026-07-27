from __future__ import annotations

from docx.text.paragraph import Paragraph as DocxParagraph

from app.engine.models.paragraph import Paragraph
from app.engine.models.page_geometry import PageGeometry
from app.engine.reader.layout_budget_reader import LayoutBudgetReader
from app.engine.reader.numbering_reader import NumberingReader
from app.engine.reader.run_reader import RunReader


class ParagraphReader:
    """
    Reads a single Word paragraph into the engine
    Paragraph model.
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

        # Reserved for future use
        _ = NumberingReader.read(docx_paragraph)

        paragraph = Paragraph(

            id=paragraph_id,

            runs=runs,

            style_name=(
                docx_paragraph.style.name
                if docx_paragraph.style
                else "Normal"
            ),

            alignment=(
                str(docx_paragraph.alignment)
                if docx_paragraph.alignment
                else None
            ),

            left_indent=(
                docx_paragraph.paragraph_format.left_indent.pt
                if docx_paragraph.paragraph_format.left_indent
                else None
            ),

            right_indent=(
                docx_paragraph.paragraph_format.right_indent.pt
                if docx_paragraph.paragraph_format.right_indent
                else None
            ),

            first_line_indent=(
                docx_paragraph.paragraph_format.first_line_indent.pt
                if docx_paragraph.paragraph_format.first_line_indent
                else None
            ),

            space_before=(
                docx_paragraph.paragraph_format.space_before.pt
                if docx_paragraph.paragraph_format.space_before
                else None
            ),

            space_after=(
                docx_paragraph.paragraph_format.space_after.pt
                if docx_paragraph.paragraph_format.space_after
                else None
            ),

            line_spacing=(
                float(docx_paragraph.paragraph_format.line_spacing)
                if docx_paragraph.paragraph_format.line_spacing
                else None
            ),

            keep_together=bool(
                docx_paragraph.paragraph_format.keep_together
            ),

            keep_with_next=bool(
                docx_paragraph.paragraph_format.keep_with_next
            ),

            page_break_before=bool(
                docx_paragraph.paragraph_format.page_break_before
            ),

            editable=True,

            section=None,
        )

        paragraph.layout_budget = LayoutBudgetReader.build(
            paragraph=paragraph,
            page_geometry=page_geometry,
            page_number=page_number,
        )

        return paragraph




