from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument

from app.engine.models.document import (
    Document,
)
from app.engine.writer.layout_writer import (
    LayoutWriter,
)


class DocxWriter:
    """
    Writes an optimized engine Document back
    to a DOCX file while preserving formatting.
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

            engine_paragraph = LayoutWriter.apply(
    paragraph=engine_paragraph,
    optimized_text=engine_paragraph.text,
)

            if not docx_paragraph.runs:

                docx_paragraph.add_run(
                    engine_paragraph.text
                )

                continue

            original_runs = len(docx_paragraph.runs)

            docx_paragraph.runs[0].text = (
                engine_paragraph.text
            )

            for run in docx_paragraph.runs[
                1:original_runs
            ]:
                run.text = ""

        doc.save(output_file)




