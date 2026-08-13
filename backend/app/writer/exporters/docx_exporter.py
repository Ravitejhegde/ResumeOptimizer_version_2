"""
app.writer.exporters.docx_exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exports the optimized DOCX document.
"""

from __future__ import annotations

from app.writer.models.write_context import (
    WriteContext,
)


class DocxExporter:
    """
    Saves the optimized DOCX.
    """

    def export(
        self,
        context: WriteContext,
    ) -> None:
        """
        Save the working document.
        """

        context.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        context.working_document.save(
            context.output_path,
        )