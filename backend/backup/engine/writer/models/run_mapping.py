from __future__ import annotations

from dataclasses import dataclass

from docx.text.run import Run as DocxRun

from app.engine.models.document.run import Run
from app.engine.writer.models.run_type import RunType


@dataclass(slots=True)
class RunMapping:
    """
    Maps one engine Run to one DOCX Run.

    This is the bridge between the engine model
    and the actual Word document.
    """

    # Engine run
    model_run: Run

    # DOCX run
    docx_run: DocxRun

    # Paragraph position
    paragraph_index: int

    # Run position inside the paragraph
    run_index: int

    # Classification of the run
    run_type: RunType = RunType.UNKNOWN

    # Whether this run can be modified
    editable: bool = True

    # Hyperlink relationship ID (if applicable)
    relationship_id: str | None = None

    # Hyperlink target URL (if applicable)
    hyperlink_target: str | None = None