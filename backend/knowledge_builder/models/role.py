from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Role:
    """
    Represents a software engineering role.

    Example:
        Backend Developer
        Frontend Developer
        DevOps Engineer
        Data Scientist
    """

    id: str

    name: str

    description: str = ""

    required_skills: list[str] = field(
        default_factory=list,
    )

    preferred_skills: list[str] = field(
        default_factory=list,
    )

    optional_skills: list[str] = field(
        default_factory=list,
    )

    tools: list[str] = field(
        default_factory=list,
    )

    responsibilities: list[str] = field(
        default_factory=list,
    )

    keywords: list[str] = field(
        default_factory=list,
    )

    aliases: list[str] = field(
        default_factory=list,
    )