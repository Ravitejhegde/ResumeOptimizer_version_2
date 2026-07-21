from dataclasses import dataclass, field

from app.services.document.snapshot.run_snapshot import (
    RunSnapshot,
)


@dataclass
class ParagraphSnapshot:

    id: str

    style: str

    text: str

    runs: list[RunSnapshot] = field(
        default_factory=list
    )