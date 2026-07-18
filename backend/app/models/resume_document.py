from dataclasses import dataclass, field


@dataclass
class Run:
    text: str

    bold: bool = False
    italic: bool = False
    underline: bool = False

    font_name: str | None = None
    font_size: float | None = None


@dataclass
class Paragraph:
    runs: list[Run] = field(default_factory=list)

    style: str = ""
    alignment: str = ""


@dataclass
class ResumeDocument:
    paragraphs: list[Paragraph] = field(default_factory=list)