from dataclasses import dataclass, field

from app.services.hyperlink.models.hyperlink import (
    Hyperlink,
)

from .document_run import (
    DocumentRun,
)

from .paragraph_format import (
    ParagraphFormat,
)


@dataclass
class DocumentBlock:
    """
    Editable document block used during optimization.

    A block represents one paragraph together with
    its runs, hyperlinks and formatting.
    """

    # -----------------------------------------
    # Identity
    # -----------------------------------------

    id: int

    paragraph_index: int

    text: str

    block_type: str

    style: str

    # -----------------------------------------
    # Runs
    # -----------------------------------------

    runs: list[DocumentRun] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Hyperlinks
    # -----------------------------------------

    hyperlinks: list[Hyperlink] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Paragraph Formatting
    # -----------------------------------------

    paragraph_format: ParagraphFormat | None = None

    # -----------------------------------------
    # Optimization
    # -----------------------------------------

    can_optimize: bool = True