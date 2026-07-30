from __future__ import annotations

import logging

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
from app.engine.writer.mappers.rewrite_mapping import (
    RewriteMapping,
)

logger = logging.getLogger(__name__)


class WriterEngine:
    """
    Final DOCX generation engine.

    Pipeline:

        OptimizationResult
                |
                v
        DocumentBuilder
                |
                v
        ParagraphUpdater
                |
                v
          RunUpdater
                |
                v
        Preservation Layer
                |
                v
          Validation
                |
                v
          DOCX Writer


    Responsibilities:

        - Coordinate writer components.
        - Preserve formatting.
        - Validate output safety.
        - Generate final DOCX.


    Does NOT:

        - Generate optimized text.
        - Analyze resume.
        - Plan changes.
    """



    def __init__(
        self,
    ) -> None:


        self._builder = (
            DocumentBuilder()
        )


        self._paragraph_updater = (
            ParagraphUpdater()
        )


        self._run_updater = (
            RunUpdater()
        )
        self._rewrite_mapping = (
            RewriteMapping()
)


        self._hyperlink_preserver = (
            HyperlinkPreserver()
        )


        self._style_preserver = (
            StylePreserver()
        )


        self._layout_preserver = (
            LayoutPreserver()
        )


        self._hyperlink_validator = (
            HyperlinkValidator()
        )


        self._structure_validator = (
            StructureValidator()
        )

        self._rewrite_mapping = (
    RewriteMapping()
)

    # --------------------------------------------------


    def write(
        self,
        result: OptimizationResult,
        source_file: str,
        output_file: str,
    ) -> None:
        """
        Generate optimized DOCX.
        """


        logger.info(
            "[Writer] Starting DOCX generation"
        )



        # ----------------------------------
        # Build writer context
        # ----------------------------------

        context = (
            self._builder.build(
                result=result,
                source_file=source_file,
            )
        )

        context = self._builder.build(
    result=result,
    source_file=source_file,
)

        self._rewrite_mapping.apply(
    rewrites=result.rewrites,
    paragraphs=context.paragraph_mappings,
)

        # ----------------------------------
        # Attach rewrite instructions
        # ----------------------------------

        self._paragraph_updater.update(
            context
        )



        # ----------------------------------
        # Update DOCX runs
        # ----------------------------------

        self._run_updater.update(
            context
        )



        # ----------------------------------
        # Preserve document features
        # ----------------------------------

        self._hyperlink_preserver.preserve(
            context
        )


        self._style_preserver.preserve(
            context
        )


        self._layout_preserver.preserve(
            context
        )



        # ----------------------------------
        # Validate final document
        # ----------------------------------

        self._hyperlink_validator.validate(
            context
        )


        self._structure_validator.validate(
            context
        )



        if not context.valid:

            logger.error(
                "[Writer] Validation failed"
            )

            raise ValueError(
                "\n".join(
                    context.errors
                )
            )



        # ----------------------------------
        # Save DOCX
        # ----------------------------------

        DocxWriter.write(
            context=context,
            output_file=output_file,
        )


        logger.info(
            "[Writer] DOCX created: %s",
            output_file,
        )