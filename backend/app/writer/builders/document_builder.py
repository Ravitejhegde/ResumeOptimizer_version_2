"""
app.writer.builders.document_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the Writer execution context.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from docx import Document

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)
from app.writer.models.write_context import (
    WriteContext,
)


class DocumentBuilder:
    """
    Creates the Writer execution context.

    Responsibilities
    ----------------
    - Load the original DOCX.
    - Create a working copy.
    - Build the WriteContext.
    """

    def build(
        self,
        source_file: str | Path,
        output_file: str | Path,
        document: DocumentModel,
        optimization: OptimizationResult,
    ) -> WriteContext:
        """
        Build a Writer context.
        """

        source_path = Path(source_file)
        output_path = Path(output_file)

        source_document = Document(source_path)

        working_document = deepcopy(
            source_document
        )

        return WriteContext(
            source_path=source_path,
            output_path=output_path,
            source_document=source_document,
            working_document=working_document,
            document=document,
            optimization=optimization,
        )