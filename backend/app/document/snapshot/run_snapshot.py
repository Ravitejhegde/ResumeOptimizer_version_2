from dataclasses import dataclass


@dataclass
class RunSnapshot:
    """
    Immutable snapshot of a Word run.
    Used throughout the optimization pipeline.
    """

    # -----------------------------------------
    # Text
    # -----------------------------------------

    text: str

    # -----------------------------------------
    # Character Formatting
    # -----------------------------------------

    bold: bool

    italic: bool

    underline: bool

    # -----------------------------------------
    # Font
    # -----------------------------------------

    font_name: str | None

    font_size: float | None

    color: str | None

    # -----------------------------------------
    # Hyperlink
    # -----------------------------------------

    hyperlink: str | None = None

    # -----------------------------------------
    # Run Control (NEW)
    # -----------------------------------------

    editable: bool = True

    object_type: str = "text"

    locked_reason: str | None = None