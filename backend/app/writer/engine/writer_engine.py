"""
app.writer.engine.writer_engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Main orchestration engine for the Writer pipeline.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)
from app.writer.builders.document_builder import (
    DocumentBuilder,
)
from app.writer.exporters.docx_exporter import (
    DocxExporter,
)
from app.writer.models.writer_result import (
    WriterResult,
)
from app.writer.rewriters.paragraph_rewriter import (
    ParagraphRewriter,
)
from app.writer.validators.document_validator import (
    DocumentValidator,
)


class WriterEngine:
    """
    Executes the Writer pipeline.
    """

    def __init__(self) -> None:
        self._builder = DocumentBuilder()
        self._rewriter = ParagraphRewriter()
        self._validator = DocumentValidator()
        self._exporter = DocxExporter()

    def write(
        self,
        source_file: str,
        output_file: str,
        document: DocumentModel,
        optimization: OptimizationResult,
    ) -> WriterResult:
        """
        Generate an optimized DOCX.
        """

        context = self._builder.build(
            source_file=source_file,
            output_file=output_file,
            document=document,
            optimization=optimization,
        )

        # Capture the original document's structural
        # and formatting fingerprint BEFORE any rewrite.
        context.format_fingerprint = (
            self._validator.create_format_fingerprint(
                context.source_document,
            )
        )

        self._rewriter.rewrite(
            context,
        )

        # Temporary diagnostic.
        print(
            "DEBUG ORIGINAL:",
            context.format_fingerprint,
        )

        print(
            "DEBUG WORKING:",
            self._validator.create_format_fingerprint(
                context.working_document,
            ),
        )

        print(
            "DEBUG MATCH:",
            self._validator.create_format_fingerprint(
                context.working_document,
            )
            == context.format_fingerprint,
        )

        self._validator.debug_format_difference(
            context.source_document,
            context.working_document,
        )

        self._validator.validate(
            context,
        )

        if context.has_errors:
            return WriterResult(
                output_path=str(output_file),
                success=False,
                message="\n".join(
                    context.errors
                ),
            )

        self._exporter.export(
            context,
        )

        return WriterResult(
            output_path=str(output_file),
            success=True,
            message=(
                "Resume written successfully."
            ),
        )