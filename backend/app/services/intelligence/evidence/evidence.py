from dataclasses import dataclass


@dataclass
class Evidence:
    """
    A single piece of evidence supporting a role.
    """

    role: str

    source: str

    confidence: int

    technology: str = ""

    section: str = ""

    explanation: str = ""