from dataclasses import dataclass, field

from app.services.document.snapshot.run_snapshot import (
    RunSnapshot,
)

from app.services.document.snapshot.hyperlink_snapshot import (
    HyperlinkSnapshot,
)


@dataclass
class ParagraphSnapshot:
    """
    Snapshot of a paragraph preserving all formatting,
    runs and hyperlinks.
    """

    id: str

    style: str

    text: str

    runs: list[RunSnapshot] = field(
        default_factory=list
    )

    hyperlinks: list[HyperlinkSnapshot] = field(
        default_factory=list
    )