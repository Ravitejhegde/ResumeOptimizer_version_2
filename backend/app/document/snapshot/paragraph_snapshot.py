from dataclasses import dataclass, field

from .run_snapshot import RunSnapshot
from app.services.hyperlink.models.hyperlink import Hyperlink


@dataclass
class ParagraphSnapshot:

    text: str

    style: str

    runs: list[RunSnapshot] = field(
        default_factory=list
    )

    hyperlinks: list[Hyperlink] = field(
        default_factory=list
    )