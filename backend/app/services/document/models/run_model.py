from dataclasses import dataclass


@dataclass
class RunModel:
    """
    Represents one text run.

    A run is the smallest editable
    text element in a Word document.
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

    # -----------------------------------------
    # Font Style
    # -----------------------------------------

    bold: bool = False

    italic: bool = False

    underline: bool = False

    strike: bool = False

    double_strike: bool = False

    superscript: bool = False

    subscript: bool = False

    all_caps: bool = False

    small_caps: bool = False

    hidden: bool = False

    outline: bool = False

    shadow: bool = False

    emboss: bool = False

    engrave: bool = False

    # -----------------------------------------
    # Colors
    # -----------------------------------------

    color: str = ""

    highlight: str = ""

    theme_color: str = ""

    # -----------------------------------------
    # Character Formatting
    # -----------------------------------------

    character_spacing: float = 0

    scale: int = 100

    kerning: float = 0

    position: float = 0

    # -----------------------------------------
    # Language
    # -----------------------------------------

    language: str = ""

    rtl: bool = False

    complex_script: bool = False

    # -----------------------------------------
    # Hyperlink
    # -----------------------------------------

    hyperlink_id: str = ""

    # -----------------------------------------
    # Style
    # -----------------------------------------

    style: str = ""

    # -----------------------------------------
    # XML Preservation
    # -----------------------------------------

    xml_properties: dict = None