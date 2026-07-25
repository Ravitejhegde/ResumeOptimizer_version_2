from dataclasses import dataclass, field


@dataclass
class AIRunUpdate:
    """
    Represents one editable run updated by AI.
    """

    index: int

    text: str


@dataclass
class AIBlockUpdate:
    """
    Represents one optimized document block.
    """

    id: int

    runs: list[AIRunUpdate] = field(
        default_factory=list
    )

    status: str = "updated"