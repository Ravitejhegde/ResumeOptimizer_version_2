from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.engine.models.document.paragraph import (
    Paragraph,
)

from app.engine.models.document.table import (
    Table,
)


@dataclass(slots=True)
class Document:
    """
    Root model representing an entire document.

    This is the canonical model exchanged
    between all engine components.
    """

    # Document content

    paragraphs: list[Paragraph] = field(
        default_factory=list,
    )

    tables: list[Table] = field(
        default_factory=list,
    )

    # Metadata

    page_count: int = 0

    section_count: int = 0

    source_path: str | None = None

    @property
    def text(
        self,
    ) -> str:
        """
        Returns the complete document text.
        """

        return "\n".join(
            paragraph.text
            for paragraph in self.paragraphs
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        """
        Returns True if the document
        contains no visible text.
        """

        return not self.text.strip()

    @property
    def paragraph_count(
        self,
    ) -> int:
        """
        Number of paragraphs.
        """

        return len(
            self.paragraphs
        )

    @property
    def table_count(
        self,
    ) -> int:
        """
        Number of tables.
        """

        return len(
            self.tables
        )




