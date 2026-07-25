from dataclasses import dataclass, field

from app.services.hyperlink.models.hyperlink_run import (
    HyperlinkRun,
)


@dataclass
class Hyperlink:
    """
    Represents one hyperlink inside a DOCX document.
    """

    # -----------------------------------------
    # Display
    # -----------------------------------------

    text: str = ""

    url: str = ""

    tooltip: str = ""

    # -----------------------------------------
    # Relationship
    # -----------------------------------------

    relationship_id: str = ""

    relationship_type: str = ""

    target_mode: str = "External"

    # -----------------------------------------
    # Hyperlink Type
    # -----------------------------------------

    is_external: bool = True

    bookmark: str = ""

    email: str = ""

    phone: str = ""

    # -----------------------------------------
    # Formatting
    # -----------------------------------------

    style: str = ""

    color: str = ""

    underline: bool = True

    visited: bool = False

    # -----------------------------------------
    # Runs
    # -----------------------------------------

    runs: list[HyperlinkRun] = field(
        default_factory=list
    )

    run_count: int = 0

    # -----------------------------------------
    # Position
    # -----------------------------------------

    paragraph_index: int = -1

    start_run: int = -1

    end_run: int = -1

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    valid: bool = True