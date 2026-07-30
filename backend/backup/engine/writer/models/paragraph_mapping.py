from __future__ import annotations

from dataclasses import dataclass, field

from docx.text.paragraph import Paragraph as DocxParagraph

from app.engine.models.document.paragraph import Paragraph
from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)
from app.engine.writer.models.run_mapping import (
    RunMapping,
)


@dataclass(slots=True)
class ParagraphMapping:
    """
    Maps one engine Paragraph to one DOCX paragraph.

    This mapping is the bridge between the
    optimization engine and the Word document.

    Every run inside the paragraph is represented
    by a RunMapping.
    """

    # Engine paragraph
    model_paragraph: Paragraph

    # Paragraph inside python-docx
    docx_paragraph: DocxParagraph

    # Paragraph position in document
    paragraph_index: int

    # Run mappings
    run_mappings: list[RunMapping] = field(
        default_factory=list,
    )
    rewrite: RewriteResult | None = None
    # Whether this paragraph should be rewritten
    editable: bool = True

    # Validation state
    valid: bool = True

    # Validation messages
    warnings: list[str] = field(
        default_factory=list,
    )