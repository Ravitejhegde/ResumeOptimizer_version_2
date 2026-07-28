from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Synonym:
    """
    Represents alternate names for a technology.
    """

    id: str

    canonical: str

    aliases: list[str] = field(
        default_factory=list,
    )