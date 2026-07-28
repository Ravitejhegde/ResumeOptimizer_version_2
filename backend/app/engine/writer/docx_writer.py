from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument

from app.engine.models.document import Document
from app.engine.writer.hyperlink_writer import (
    HyperlinkWriter,
)
from app.engine.writer.layout_writer import (
    LayoutWriter,
)
from app.engine.writer.numbering_writer import (
    NumberingWriter,
)
from app.engine.writer.style_writer import (
    StyleWriter,
)


class DocxWriter:
    """
    Writes an optimized engine Document
    back to a DOCX file.

    Responsibilities
    ----------------
    • Open original DOCX
    • Coordinate writer stages
    • Save optimized DOCX

    Individual writers preserve their
    own responsibilities.
    """

    @staticmethod
    def write(
        document: Document,
        source_file: str,
        output_file: str,
    ) -> None:

        source_path = Path(source_file)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source document not found: {source_file}"
            )

        doc = DocxDocument(source_file)

        paragraph_count = min(
            len(doc.paragraphs),
            len(document.paragraphs),
        )

        for index in range(paragraph_count):

            docx_paragraph = doc.paragraphs[index]

            engine_paragraph = document.paragraphs[index]

            # ----------------------------------
            # Update engine paragraph
            # ----------------------------------

            updated = LayoutWriter.apply(
                paragraph=engine_paragraph,
                optimized_text=engine_paragraph.text,
            )

            if not docx_paragraph.runs:
                docx_paragraph.add_run(updated.text)

            else:

                original_run = docx_paragraph.runs[0]

                original_run.text = updated.text

                for run in docx_paragraph.runs[1:]:
                    run.text = ""

                StyleWriter.apply(
                    source=original_run,
                    target=original_run,
                )

            # ----------------------------------
            # Preserve document structures
            # ----------------------------------

            HyperlinkWriter.apply(
                source=docx_paragraph,
                target=docx_paragraph,
            )

            NumberingWriter.apply(
                source=docx_paragraph,
                target=docx_paragraph,
            )

        doc.save(output_file)