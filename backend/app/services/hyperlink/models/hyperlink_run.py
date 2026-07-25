from dataclasses import dataclass


@dataclass
class HyperlinkRun:
    """
    Represents one run inside a hyperlink.

    Word may split a hyperlink into multiple runs,
    each with different formatting.
    """

    # -----------------------------------------
    # Text
    # -----------------------------------------

    text: str = ""

    # -----------------------------------------
    # Font
    # -----------------------------------------

    font_name: str = ""

    font_size: float = 0

    style: str = ""

    # -----------------------------------------
    # Formatting
    # -----------------------------------------

    bold: bool = False

    italic: bool = False

    underline: bool = True

    color: str = ""

    # -----------------------------------------
    # Position
    # -----------------------------------------

    run_index: int = -1