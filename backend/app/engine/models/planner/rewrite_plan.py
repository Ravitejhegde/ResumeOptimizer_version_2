from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewritePlan:
    """
    One rewrite instruction.
    """

    paragraph_id: str

    section: str

    technology: str

    action: str

    priority: int

    reason: str
