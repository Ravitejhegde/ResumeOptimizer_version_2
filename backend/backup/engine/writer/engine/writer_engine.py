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
from app.engine.writer.preservers.hyperlink_preserver import (
    HyperlinkPreserver,
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
from app.engine.writer.validators.hyperlink_validator import (
    HyperlinkValidator,
)
from app.engine.writer.validators.structure_validator import (
    StructureValidator,
)


class WriterEngine:
    """
    Coordinates the complete Writer pipeline.
    """

    def __init__(self) -> None:

        self._builder = DocumentBuilder()

        self._paragraph_updater = ParagraphUpdater()

        self._run_updater = RunUpdater()

        self._hyperlink_preserver = HyperlinkPreserver()

        self._style_preserver = StylePreserver()

        self._layout_preserver = LayoutPreserver()

        self._hyperlink_validator = HyperlinkValidator()

        self._structure_validator = StructureValidator()

    def write(
        self,
        result: OptimizationResult,
        source_file: str,
        output_file: str,
    ) -> None:

        context = self._builder.build(
            result=result,
            source_file=source_file,
        )

        self._paragraph_updater.update(context)

        self._run_updater.update(context)

        self._hyperlink_preserver.preserve(context)

        self._style_preserver.preserve(context)

        self._layout_preserver.preserve(context)

        self._hyperlink_validator.validate(context)

        self._structure_validator.validate(context)

        if not context.valid:
            raise ValueError(
                "\n".join(context.errors)
            )

        DocxWriter.write(
            context=context,
            output_file=output_file,
        )