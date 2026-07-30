from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StructureAnalysis:
    """
    Structural analysis of a resume document.

    Represents document organization,
    detected sections, and structural quality.

    Used by:
        - Analyzer
        - ATS Analysis
        - Planner
    """

    # --------------------------------------------------
    # Document Metrics
    # --------------------------------------------------

    paragraph_count: int = 0

    run_count: int = 0

    table_count: int = 0

    section_count: int = 0

    empty_paragraphs: int = 0

    # --------------------------------------------------
    # Detected Sections
    # --------------------------------------------------

    sections: list[str] = field(
        default_factory=list,
    )

    section_distribution: dict[
        str,
        int,
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Section Intelligence
    # --------------------------------------------------

    headings: list[str] = field(
        default_factory=list,
    )

    missing_sections: list[str] = field(
        default_factory=list,
    )

    section_confidence: float = 0.0

    # --------------------------------------------------
    # Quality Information
    # --------------------------------------------------

    warnings: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_section(
        self,
        section_name: str,
    ) -> bool:

        normalized = section_name.lower()

        return any(
            section.lower() == normalized
            for section in self.sections
        )

    def section_count_by_name(
        self,
        section_name: str,
    ) -> int:

        return self.section_distribution.get(
            section_name,
            0,
        )