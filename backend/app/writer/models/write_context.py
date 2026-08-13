"""
app.writer.models.write_context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shared execution context for the Writer pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from docx.document import Document as DocxDocument

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)


@dataclass(slots=True)
class WriteContext:
    """
    Shared context passed through the Writer pipeline.

    Responsibilities
    ----------------
    - Hold source and working DOCX.
    - Hold parsed document model.
    - Hold optimization result.
    - Track paragraph mappings.
    - Track warnings/errors.
    """

    # -------------------------------------------------
    # File Information
    # -------------------------------------------------

    source_path: Path

    output_path: Path

    # -------------------------------------------------
    # DOCX Documents
    # -------------------------------------------------

    source_document: DocxDocument

    working_document: DocxDocument

    # -------------------------------------------------
    # Parsed Resume
    # -------------------------------------------------

    document: DocumentModel

    # -------------------------------------------------
    # Optimizer Output
    # -------------------------------------------------

    optimization: OptimizationResult

    # -------------------------------------------------
    # Writer State
    # -------------------------------------------------

    paragraph_map: dict[str, int] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    valid: bool = True

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(message)

    def add_error(
        self,
        message: str,
    ) -> None:
        self.errors.append(message)
        self.valid = False

    @property
    def has_errors(
        self,
    ) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(
        self,
    ) -> bool:
        return bool(self.warnings)