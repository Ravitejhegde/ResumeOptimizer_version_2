from dataclasses import dataclass, field


@dataclass
class RunNode:
    text: str
    bold: bool
    italic: bool
    underline: bool


@dataclass
class ParagraphNode:
    runs: list[RunNode] = field(default_factory=list)


@dataclass
class DocumentNode:
    paragraphs: list[ParagraphNode] = field(default_factory=list)




