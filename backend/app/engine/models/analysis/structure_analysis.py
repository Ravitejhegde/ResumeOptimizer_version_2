from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StructureAnalysis:
    """
    Structural analysis of a document.
    """

    paragraph_count: int = 0

    run_count: int = 0

    table_count: int = 0

    section_count: int = 0

    empty_paragraphs: int = 0

    sections: list[str] = field(
        default_factory=list,
    )

    section_distribution: dict[
        str,
        int,
    ] = field(
        default_factory=dict,
    )
