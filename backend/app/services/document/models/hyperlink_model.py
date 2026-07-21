from dataclasses import dataclass


@dataclass
class HyperlinkModel:
    """
    Represents one hyperlink in a Word document.
    """

    # -----------------------------------------
    # Display
    # -----------------------------------------

    text: str = ""

    url: str = ""

    tooltip: str = ""

    # -----------------------------------------
    # Type
    # -----------------------------------------

    is_external: bool = True

    bookmark: str = ""

    email: str = ""

    phone: str = ""

    # -----------------------------------------
    # Relationship
    # -----------------------------------------

    relationship_id: str = ""

    # -----------------------------------------
    # Formatting
    # -----------------------------------------

    color: str = ""

    underline: bool = True

    visited: bool = False

    style: str = ""

    # -----------------------------------------
    # Position
    # -----------------------------------------

    paragraph_id: int = -1

    run_index: int = -1