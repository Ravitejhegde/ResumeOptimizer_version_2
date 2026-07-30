from __future__ import annotations

from dataclasses import dataclass, field

from docx.document import (
    Document as DocxDocument,
)

from app.engine.models.document.document import (
    Document,
)

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)

from app.engine.writer.models.paragraph_mapping import (
    ParagraphMapping,
)


@dataclass(slots=True)
class WriteContext:
    """
    Shared context for Writer pipeline.

    Pipeline:

        OptimizationResult
                |
                v
          WriteContext
                |
                v
        ParagraphUpdater
                |
                v
          RunUpdater
                |
                v
          DOCX Writer


    Responsibilities:

        - Hold source DOCX.
        - Hold working DOCX.
        - Hold engine document models.
        - Hold optimization results.
        - Hold paragraph mappings.
        - Track writer validation state.


    Does NOT:

        - Generate optimization text.
        - Analyze resume.
        - Decide rewrites.
    """


    # ----------------------------------
    # DOCX Documents
    # ----------------------------------

    source_doc: DocxDocument

    working_doc: DocxDocument


    # ----------------------------------
    # Engine Document Models
    # ----------------------------------

    source_model: Document

    working_model: Document


    # ----------------------------------
    # Optimization Output
    # ----------------------------------

    optimization: OptimizationResult


    # ----------------------------------
    # Mapping Layer
    # ----------------------------------

    paragraph_mappings: list[
        ParagraphMapping
    ] = field(
        default_factory=list,
    )


    # ----------------------------------
    # Validation State
    # ----------------------------------

    warnings: list[str] = field(
        default_factory=list,
    )


    errors: list[str] = field(
        default_factory=list,
    )


    valid: bool = True



    # ----------------------------------
    # Helpers
    # ----------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Add non-blocking warning.
        """

        self.warnings.append(
            message
        )



    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Add blocking writer error.
        """

        self.errors.append(
            message
        )

        self.valid = False



    def has_errors(
        self,
    ) -> bool:
        """
        Check whether writer has errors.
        """

        return bool(
            self.errors
        )



    def has_rewrites(
        self,
    ) -> bool:
        """
        Check whether optimizer
        produced rewrite results.
        """

        return bool(
            self.optimization.rewrites
        )


    def rewrite_count(
        self,
    ) -> int:
        """
        Number of rewrite operations.
        """

        return len(
            self.optimization.rewrites
        )