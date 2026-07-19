from dataclasses import dataclass


@dataclass
class Skill:

    name: str

    category: str

    section: str

    source: str

    score: int = 0

    keep: bool = False

    remove: bool = False

    add: bool = False