from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ATSAnalysis:
    """
    Result of ATS compatibility analysis.
    """

    score: int = 0

    is_ats_friendly: bool = False

    required_sections: list[str] = field(
        default_factory=list,
    )

    missing_sections: list[str] = field(
        default_factory=list,
    )

    paragraph_count: int = 0

    empty_paragraphs: int = 0

    has_tables: bool = False

    warnings: list[str] = field(
        default_factory=list,
    )
