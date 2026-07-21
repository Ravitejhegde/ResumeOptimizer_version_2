from dataclasses import dataclass, field

from app.services.document.snapshot.paragraph_snapshot import (
    ParagraphSnapshot,
)


@dataclass
class DocumentSnapshot:
    """
    Immutable representation of a document.

    Used by the Intelligence Engine.

    Never edits Word directly.
    """

    paragraphs: list[ParagraphSnapshot] = field(
        default_factory=list
    )