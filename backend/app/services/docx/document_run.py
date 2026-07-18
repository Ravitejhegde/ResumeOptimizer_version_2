from dataclasses import dataclass


@dataclass
class DocumentRun:

    # -----------------------------
    # Text
    # -----------------------------

    text: str

    # -----------------------------
    # Character formatting
    # -----------------------------

    bold: bool

    italic: bool

    underline: bool

    strike: bool = False

    superscript: bool = False

    subscript: bool = False

    all_caps: bool = False

    small_caps: bool = False

    hidden: bool = False

    # -----------------------------
    # Font
    # -----------------------------

    font_name: str | None = None

    font_size: float | None = None

    color: str | None = None

    highlight_color: str | None = None

    # -----------------------------
    # Hyperlink
    # -----------------------------

    hyperlink: str | None = None

    # -----------------------------
    # Style
    # -----------------------------

    style_name: str | None = None