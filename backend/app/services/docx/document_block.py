from dataclasses import dataclass, field

from .document_run import DocumentRun
from .paragraph_format import ParagraphFormat


@dataclass
class DocumentBlock:

    id: int

    paragraph_index: int

    text: str

    block_type: str

    style: str

    runs: list[DocumentRun] = field(
        default_factory=list
    )

    paragraph_format: ParagraphFormat | None = None

    can_optimize: bool = True