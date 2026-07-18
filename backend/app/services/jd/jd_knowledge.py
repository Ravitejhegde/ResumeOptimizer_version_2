from dataclasses import dataclass, field


@dataclass
class JDKnowledge:

    required: set[str] = field(
        default_factory=set
    )

    preferred: set[str] = field(
        default_factory=set
    )

    responsibilities: list[str] = field(
        default_factory=list
    )