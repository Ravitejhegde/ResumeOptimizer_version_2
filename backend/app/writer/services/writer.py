"""
app.writer.services.writer
~~~~~~~~~~~~~~~~~~~~~~~~~~

Public Writer service.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)
from app.writer.engine.writer_engine import (
    WriterEngine,
)
from app.writer.models.writer_result import (
    WriterResult,
)


class Writer:
    """
    Public Writer API.
    """

    def __init__(
        self,
    ) -> None:

        self._engine = WriterEngine()

    def write(
        self,
        source_file: str,
        output_file: str,
        document: DocumentModel,
        optimization: OptimizationResult,
    ) -> WriterResult:

        return self._engine.write(
            source_file=source_file,
            output_file=output_file,
            document=document,
            optimization=optimization,
        )