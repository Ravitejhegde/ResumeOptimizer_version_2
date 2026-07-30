from __future__ import annotations

from dataclasses import dataclass, field

from docx.text.paragraph import Paragraph as DocxParagraph

from app.engine.models.document.paragraph import (
    Paragraph,
)

from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)

from app.engine.writer.models.run_mapping import (
    RunMapping,
)


@dataclass(slots=True)
class ParagraphMapping:
    """
    Bridge between engine paragraph
    and DOCX paragraph.

    Flow:

        Document Model
              |
              v
       ParagraphMapping
              |
              v
        RunMappings
              |
              v
          DOCX Writer


    Responsibilities:

        - Keep relationship between
          engine paragraph and DOCX paragraph.
        - Store rewrite instruction.
        - Track editable state.
        - Track validation state.


    Does NOT:

        - Generate text.
        - Modify DOCX.
        - Decide optimization.
    """


    # ----------------------------------
    # Engine Paragraph
    # ----------------------------------

    model_paragraph: Paragraph



    # ----------------------------------
    # python-docx Paragraph
    # ----------------------------------

    docx_paragraph: DocxParagraph



    # ----------------------------------
    # Location
    # ----------------------------------

    paragraph_index: int



    # ----------------------------------
    # Run Mapping
    # ----------------------------------

    run_mappings: list[
        RunMapping
    ] = field(
        default_factory=list,
    )



    # ----------------------------------
    # Rewrite Information
    # ----------------------------------

    rewrite: RewriteResult | None = None



    # ----------------------------------
    # Writer Control
    # ----------------------------------

    editable: bool = True



    # ----------------------------------
    # Validation
    # ----------------------------------

    valid: bool = True


    warnings: list[str] = field(
        default_factory=list,
    )


    errors: list[str] = field(
        default_factory=list,
    )



    # ----------------------------------
    # Helpers
    # ----------------------------------

    def attach_rewrite(
        self,
        rewrite: RewriteResult,
    ) -> None:
        """
        Attach optimization result.
        """

        self.rewrite = rewrite

        self.editable = True



    def disable_editing(
        self,
        reason: str | None = None,
    ) -> None:
        """
        Prevent modification.
        """

        self.editable = False

        if reason:

            self.warnings.append(
                reason
            )



    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(
            message
        )



    def add_error(
        self,
        message: str,
    ) -> None:

        self.errors.append(
            message
        )

        self.valid = False



    def has_rewrite(
        self,
    ) -> bool:
        """
        Check if paragraph
        has optimization change.
        """

        return (
            self.rewrite is not None
            and
            self.rewrite.success
        )