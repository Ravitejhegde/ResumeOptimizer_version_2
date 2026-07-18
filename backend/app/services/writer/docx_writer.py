from pathlib import Path

from docx import Document

from app.services.docx.document_block import DocumentBlock


class DocxWriter:

    @staticmethod
    def write(
        input_path: str | Path,
        blocks: list[DocumentBlock],
        output_path: str | Path,
    ):

        document = Document(input_path)

        for block in blocks:

            paragraph = document.paragraphs[
                block.paragraph_index
            ]

            paragraph.text = block.text

        document.save(output_path)