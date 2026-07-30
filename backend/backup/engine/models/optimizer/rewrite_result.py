from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RewriteResult:
    """
    Result of rewriting one paragraph.

    Produced by Optimizer.

    Used by:
        - Validation
        - Writer
        - Reporting
    """

    paragraph_id: str

    success: bool

    original_text: str

    optimized_text: str

    reason: str = ""

    confidence: float = 0.0

    formatting_preserved: bool = True

    original_length: int = 0

    optimized_length: int = 0

    @property
    def length_difference(
        self,
    ) -> int:

        return (
            self.optimized_length
            -
            self.original_length
        )