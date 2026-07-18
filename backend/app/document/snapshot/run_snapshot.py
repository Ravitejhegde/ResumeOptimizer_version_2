from dataclasses import dataclass


@dataclass
class RunSnapshot:

    text: str

    bold: bool

    italic: bool

    underline: bool

    font_name: str | None

    font_size: float | None

    color: str | None