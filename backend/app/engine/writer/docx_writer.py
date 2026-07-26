from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument

from app.engine.models.document import Document
from app.engine.writer.layout_writer import LayoutWriter


class DocxWriter:
    """
    Writes the optimized document back to a DOCX file.

    Responsibilities
    ----------------
    - Preserve document formatting
    - Preserve paragraph order
    - Preserve run formatting
    - Preserve hyperlinks
    - Save optimized document

    This class NEVER performs optimization.
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

            optimized_text = engine_paragraph.text

            # Apply optimized text while preserving
            # formatting information stored in the
            # engine paragraph.
            LayoutWriter.apply(
                engine_paragraph,
                optimized_text,
            )

            if docx_paragraph.runs:

                docx_paragraph.runs[0].text = optimized_text

                for run in docx_paragraph.runs[1:]:

                    run.text = ""

            else:

                docx_paragraph.add_run(
                    optimized_text
                )

        doc.save(output_file)