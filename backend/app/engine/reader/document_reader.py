from __future__ import annotations

from docx import Document as DocxDocument

from app.engine.models.document import Document
from app.engine.reader.metadata_reader import MetadataReader
from app.engine.reader.page_geometry_reader import (
    PageGeometryReader,
)
from app.engine.reader.paragraph_reader import ParagraphReader
from app.engine.reader.table_reader import TableReader


class DocumentReader:
    """
    Reads an entire DOCX document into the engine Document model.
    """

    @staticmethod
    def read(
        file_path: str,
    ) -> Document:

        docx_document = DocxDocument(file_path)

        metadata = MetadataReader.read(
            document=docx_document,
            source_path=file_path,
        )

        document = Document(
            source_path=metadata["source_path"],
            section_count=len(docx_document.sections),
        )

        # ----------------------------------------
        # Page Geometry
        # ----------------------------------------

        if not docx_document.sections:
            raise ValueError(
                "The document contains no sections."
            )

        page_geometry = PageGeometryReader.read(
            docx_document.sections[0]
        )

        page_number = 1

        # ----------------------------------------
        # Paragraphs
        # ----------------------------------------

        for index, paragraph in enumerate(
            docx_document.paragraphs,
            start=1,
        ):

            document.paragraphs.append(
                ParagraphReader.read(
                    docx_paragraph=paragraph,
                    paragraph_id=f"P{index:05}",
                    page_geometry=page_geometry,
                    page_number=page_number,
                )
            )

        # ----------------------------------------
        # Tables
        # ----------------------------------------

        for index, table in enumerate(
            docx_document.tables,
            start=1,
        ):

            document.tables.append(
                TableReader.read(
                    docx_table=table,
                    table_id=f"T{index:03}",
                )
            )

        return document