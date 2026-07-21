from dataclasses import dataclass


@dataclass
class RunSnapshot:

    text: str

    bold: bool

    italic: bool

    underline: bool

    font: str

    size: float