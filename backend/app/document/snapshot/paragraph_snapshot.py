from dataclasses import dataclass, field

from .run_snapshot import RunSnapshot


@dataclass
class ParagraphSnapshot:

    text: str

    style: str

    runs: list[RunSnapshot] = field(
        default_factory=list
    )