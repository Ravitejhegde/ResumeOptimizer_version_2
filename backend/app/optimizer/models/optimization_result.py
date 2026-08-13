"""
app.optimizer.models.optimization_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the final output produced by the Optimizer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.optimizer.models.paragraph_update import (
    ParagraphUpdate,
)


@dataclass(slots=True)
class OptimizationResult:
    """
    Final optimization result.

    Produced by:
        - OptimizerEngine

    Consumed by:
        - Writer
    """

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    document: DocumentModel

    # -------------------------------------------------
    # AI Updates
    # -------------------------------------------------

    paragraph_updates: list[
        ParagraphUpdate
    ] = field(
        default_factory=list
    )

    # -------------------------------------------------
    # Diagnostics
    # -------------------------------------------------

    warnings: list[str] = field(
        default_factory=list
    )

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    success: bool = False

    message: str = ""

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    @property
    def updated_paragraphs(
        self,
    ) -> int:
        """
        Number of paragraphs updated.
        """

        return len(
            self.paragraph_updates
        )

    @property
    def changed_paragraphs(
        self,
    ) -> int:
        """
        Number of paragraphs whose content changed.
        """

        return sum(
            update.changed
            for update in self.paragraph_updates
        )

    @property
    def has_updates(
        self,
    ) -> bool:
        """
        True if there are paragraph updates.
        """

        return bool(
            self.paragraph_updates
        )