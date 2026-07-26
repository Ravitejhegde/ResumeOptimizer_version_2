from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KeywordAnalysisResult:
    """
    Result produced by KeywordAnalyzer.
    """

    detected_skills: list[str] = field(
        default_factory=list
    )

    normalized_skills: list[str] = field(
        default_factory=list
    )

    categorized_skills: dict[str, list[str]] = field(
        default_factory=dict
    )

    duplicate_skills: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class ATSAnalysisResult:
    """
    Result produced by ATSAnalyzer.
    """

    score: int

    required_sections: list[str]

    missing_sections: list[str]

    has_tables: bool

    paragraph_count: int

    empty_paragraphs: int

    is_ats_friendly: bool


@dataclass(slots=True)
class StructureAnalysisResult:
    """
    Result produced by StructureAnalyzer.
    """

    sections: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class AnalysisResult:
    """
    Complete document analysis.
    """

    keywords: KeywordAnalysisResult

    structure: StructureAnalysisResult

    ats: ATSAnalysisResult