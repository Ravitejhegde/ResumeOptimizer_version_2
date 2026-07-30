from __future__ import annotations

from dataclasses import dataclass, field

from docx.text.run import Run as DocxRun

from app.engine.models.document.run import (
    Run,
)

from app.engine.writer.models.run_type import (
    RunType,
)


@dataclass(slots=True)
class RunMapping:
    """
    Maps one engine Run to one DOCX Run.

    Bridge:

        Engine Run
             |
             v
        RunMapping
             |
             v
        python-docx Run


    Responsibilities:

        - Preserve run relationship.
        - Track formatting unit.
        - Track hyperlink information.
        - Control edit permission.


    Does NOT:

        - Generate text.
        - Decide optimization.
        - Modify DOCX.
    """


    # ----------------------------------
    # Engine Model
    # ----------------------------------

    model_run: Run



    # ----------------------------------
    # DOCX Object
    # ----------------------------------

    docx_run: DocxRun



    # ----------------------------------
    # Position
    # ----------------------------------

    paragraph_index: int

    run_index: int



    # ----------------------------------
    # Run Classification
    # ----------------------------------

    run_type: RunType = RunType.UNKNOWN



    # ----------------------------------
    # Modification Control
    # ----------------------------------

    editable: bool = True



    # ----------------------------------
    # Hyperlink Support
    # ----------------------------------

    relationship_id: str | None = None

    hyperlink_target: str | None = None



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

    def disable_editing(
        self,
        reason: str | None = None,
    ) -> None:
        """
        Prevent modification of this run.
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



    def has_hyperlink(
        self,
    ) -> bool:
        """
        Check whether run contains hyperlink.
        """

        return (
            self.hyperlink_target
            is not None
        )