from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewriteResult:
    """
    Result of rewriting one paragraph.
    """

    paragraph_id: str

    success: bool

    original_text: str

    optimized_text: str

    reason: str = ""
