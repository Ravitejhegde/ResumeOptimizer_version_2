from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from docx import Document as DocxDocument

from app.engine.models.document.document import (
    Document,
)


class DocxWriter:
    """
    Writes optimized text back into the
    original DOCX while preserving layout.

    This class never changes formatting.
    """

    # --------------------------------------------------

    @staticmethod
    def write(
        document: Document,
        source_file: str,
        output_file: str,
    ) -> None:

        doc = DocxDocument(
            source_file,
        )

        paragraphs = list(
            doc.paragraphs,
        )

        for model, paragraph in zip(
            document.paragraphs,
            paragraphs,
        ):

            if not paragraph.runs:
                continue

            paragraph.runs[0].text = model.text

            for run in paragraph.runs[1:]:

                run.text = ""

        Path(
            output_file,
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        doc.save(
            output_file,
        )
