from dataclasses import dataclass


@dataclass
class RunSnapshot:

    # -----------------------------
    # Text
    # -----------------------------

    text: str

    # -----------------------------
    # Character Formatting
    # -----------------------------

    bold: bool

    italic: bool

    underline: bool

    # -----------------------------
    # Font
    # -----------------------------

    font_name: str | None

    font_size: float | None

    color: str | None

    # -----------------------------
    # Hyperlink
    # -----------------------------

    hyperlink: str | None = None