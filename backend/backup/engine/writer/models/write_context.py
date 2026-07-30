from __future__ import annotations

from dataclasses import dataclass, field

from docx.document import Document as DocxDocument

from app.engine.models.document.document import Document
from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)
from app.engine.writer.models.paragraph_mapping import (
    ParagraphMapping,
)


@dataclass
class WriteContext:
    """
    Shared context for the complete Writer pipeline.

    Every writer component reads from and updates this object.
    """

    # Original DOCX loaded from disk
    source_doc: DocxDocument

    # Working DOCX (modified during writing)
    working_doc: DocxDocument

    # Original document model
    source_model: Document

    # Working document model
    working_model: Document

    # Optimization output
    optimization: OptimizationResult

    # Mapping between model runs and DOCX runs
    paragraph_mappings: list[ParagraphMapping] = field(
    default_factory=list,
)

    # Validation warnings
    warnings: list[str] = field(
        default_factory=list
    )

    # Validation errors
    errors: list[str] = field(
        default_factory=list
    )

    # Whether the document is safe to save
    valid: bool = True