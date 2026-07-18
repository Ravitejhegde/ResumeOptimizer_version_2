from dataclasses import dataclass, field

from .paragraph_snapshot import (
    ParagraphSnapshot,
)


@dataclass
class DocumentSnapshot:

    paragraphs: list[
        ParagraphSnapshot
    ] = field(
        default_factory=list
    )