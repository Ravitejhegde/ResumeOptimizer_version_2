from dataclasses import dataclass


@dataclass
class DocumentRun:
    """
    Represents a single run inside a paragraph.

    A run can be editable text or a locked object
    such as a hyperlink.
    """

    # -----------------------------------------
    # Text
    # -----------------------------------------

    text: str

    # -----------------------------------------
    # Character formatting
    # -----------------------------------------

    bold: bool

    italic: bool

    underline: bool

    strike: bool = False

    superscript: bool = False

    subscript: bool = False

    all_caps: bool = False

    small_caps: bool = False

    hidden: bool = False

    # -----------------------------------------
    # Font
    # -----------------------------------------

    font_name: str | None = None

    font_size: float | None = None

    color: str | None = None

    highlight_color: str | None = None

    # -----------------------------------------
    # Hyperlink
    # -----------------------------------------

    hyperlink: str | None = None

    # -----------------------------------------
    # Style
    # -----------------------------------------

    style_name: str | None = None

    # -----------------------------------------
    # Run Control (NEW)
    # -----------------------------------------

    editable: bool = True

    object_type: str = "text"
    # text
    # hyperlink
    # image
    # field
    # bookmark
    # etc.

    locked_reason: str | None = None