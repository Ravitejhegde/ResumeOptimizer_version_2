from __future__ import annotations

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)
from app.engine.writer.builders.document_builder import (
    DocumentBuilder,
)
from app.engine.writer.docx_writer import (
    DocxWriter,
)
from app.engine.writer.preservers.layout_preserver import (
    LayoutPreserver,
)
from app.engine.writer.preservers.style_preserver import (
    StylePreserver,
)
from app.engine.writer.updaters.paragraph_updater import (
    ParagraphUpdater,
)
from app.engine.writer.updaters.run_updater import (
    RunUpdater,
)


class WriterEngine:
    """
    Final stage of the Resume Optimization pipeline.

    OptimizationResult
            │
            ▼
    DocumentBuilder
            │
            ▼
    ParagraphUpdater
            │
            ▼
    RunUpdater
            │
            ▼
    StylePreserver
            │
            ▼
    LayoutPreserver
            │
            ▼
        DocxWriter
    """

    def __init__(
        self,
    ) -> None:

        self._builder = DocumentBuilder()

        self._paragraph_updater = (
            ParagraphUpdater()
        )

        self._run_updater = (
            RunUpdater()
        )

        self._style_preserver = (
            StylePreserver()
        )

        self._layout_preserver = (
            LayoutPreserver()
        )

    # --------------------------------------------------

    def write(
        self,
        result: OptimizationResult,
        source_file: str,
        output_file: str,
    ) -> None:

        document = self._builder.build(
            result,
        )

        for rewrite in result.rewrites:

            paragraph = next(
                (
                    p
                    for p in document.paragraphs
                    if p.id == rewrite.paragraph_id
                ),
                None,
            )

            if paragraph is None:

                continue

            self._paragraph_updater.update(
                paragraph,
                rewrite,
            )

            self._run_updater.update(
                paragraph.runs,
                rewrite.optimized_text,
            )

            self._style_preserver.preserve(
                paragraph,
                paragraph,
            )

        document = self._layout_preserver.preserve(
            result.document,
            document,
        )

        DocxWriter.write(
            document=document,
            source_file=source_file,
            output_file=output_file,
        )
