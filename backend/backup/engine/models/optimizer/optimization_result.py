from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


@dataclass(slots=True)
class OptimizationResult:
    """
    Final output produced by Optimizer.

    Contains the optimized document and
    all applied changes.
    """

    document: Document

    rewrites: list[RewriteResult] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    success: bool = True

    validation_passed: bool = False

    changed_paragraphs: int = 0

    @property
    def rewrite_count(
        self,
    ) -> int:

        return len(
            self.rewrites
        )