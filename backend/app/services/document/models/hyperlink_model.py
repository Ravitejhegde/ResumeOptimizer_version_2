from dataclasses import dataclass


@dataclass
class HyperlinkModel:
    """
    Represents a hyperlink extracted from a Word document.
    Preserves both hyperlink metadata and its position so it
    can be recreated exactly during document generation.
    """

    # -----------------------------------------
    # Display
    # -----------------------------------------

    text: str = ""
    url: str = ""
    tooltip: str = ""

    # -----------------------------------------
    # Hyperlink Type
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
    # Document Position
    # -----------------------------------------

    paragraph_id: int = -1

    # A hyperlink may span multiple runs
    start_run: int = -1
    end_run: int = -1