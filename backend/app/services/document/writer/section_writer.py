from docx.document import Document as DocxDocument
from docx.enum.section import WD_SECTION

from app.services.document.models.section_model import (
    SectionModel,
)

from app.services.document.writer.paragraph_writer import (
    ParagraphWriter,
)

from app.services.document.writer.table_writer import (
    TableWriter,
)


class SectionWriter:
    """
    Writes SectionModel objects into a DOCX document.
    """

    @classmethod
    def write(
        cls,
        document: DocxDocument,
        sections: list[SectionModel],
    ) -> None:

        first = True

        for section_model in sections:

            # -----------------------------------------
            # Create Section
            # -----------------------------------------

            if not first:

                document.add_section(
                    WD_SECTION.CONTINUOUS
                )

            first = False

            section = document.sections[-1]

            # -----------------------------------------
            # Page Layout
            # -----------------------------------------

            try:
                section.page_width = section_model.page_width
            except Exception:
                pass

            try:
                section.page_height = section_model.page_height
            except Exception:
                pass

            try:
                section.left_margin = section_model.margin_left
                section.right_margin = section_model.margin_right
                section.top_margin = section_model.margin_top
                section.bottom_margin = section_model.margin_bottom
            except Exception:
                pass

            # -----------------------------------------
            # Paragraphs
            # -----------------------------------------

            ParagraphWriter.write(
                document,
                section_model.paragraphs,
            )

            # -----------------------------------------
            # Tables
            # -----------------------------------------

            TableWriter.write(
                document,
                section_model.tables,
            )