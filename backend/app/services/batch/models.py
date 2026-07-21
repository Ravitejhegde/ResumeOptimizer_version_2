from dataclasses import dataclass


@dataclass
class AIBlockUpdate:

    id: int

    text: str

    status: str = "updated"