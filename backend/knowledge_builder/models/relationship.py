from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Relationship:
    """
    Represents a relationship between two technologies.

    Example:

    Python ----uses----> FastAPI

    React ----depends_on----> TypeScript
    """

    source: str

    target: str

    relation: str

    weight: float = 1.0