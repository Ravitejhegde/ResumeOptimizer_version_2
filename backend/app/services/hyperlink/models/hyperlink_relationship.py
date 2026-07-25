from dataclasses import dataclass


@dataclass
class HyperlinkRelationship:
    """
    Represents a DOCX hyperlink relationship.

    Maps a relationship ID (rId) to its target URL.
    """

    # -----------------------------------------
    # Relationship
    # -----------------------------------------

    relationship_id: str = ""

    relationship_type: str = ""

    target_mode: str = "External"

    # -----------------------------------------
    # Target
    # -----------------------------------------

    url: str = ""

    # -----------------------------------------
    # Metadata
    # -----------------------------------------

    is_external: bool = True

    is_valid: bool = True