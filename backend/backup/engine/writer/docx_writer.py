from __future__ import annotations

from pathlib import Path

from app.engine.writer.models.write_context import (
    WriteContext,
)


class DocxWriter:
    """
    Final stage of the Writer pipeline.

    Responsible only for saving the working document.
    """

    @staticmethod
    def write(
        context: WriteContext,
        output_file: str,
    ) -> None:

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        context.working_doc.save(
            output_file,
        )