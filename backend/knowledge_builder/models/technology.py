from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Technology:
    """
    Represents a single technology.

    Example:
        Python
        React
        PostgreSQL
        Docker
    """

    id: str

    name: str

    category: str

    aliases: list[str] = field(
        default_factory=list,
    )

    tags: list[str] = field(
        default_factory=list,
    )

    description: str = ""

    related: list[str] = field(
        default_factory=list,
    )

    official_url: str | None = None