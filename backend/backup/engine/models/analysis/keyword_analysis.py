from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KeywordAnalysis:
    """
    Technology and keyword extraction result.

    Produced by Analyzer.

    Used by:
        - Skill Comparator
        - Intelligence Engine
        - Planner

    Stores:
        - detected keywords
        - normalized skills
        - duplicate detection
        - skill categories
        - confidence
        - extraction sources
    """

    # --------------------------------------------------
    # Raw Detection
    # --------------------------------------------------

    detected: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Knowledge Normalized Skills
    # --------------------------------------------------

    normalized: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Duplicate / Noise Detection
    # --------------------------------------------------

    duplicates: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Skill Classification
    # --------------------------------------------------

    categories: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    confidence: dict[
        str,
        float,
    ] = field(
        default_factory=dict,
    )

    sources: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def get_confidence(
        self,
        keyword: str,
    ) -> float:

        return self.confidence.get(
            keyword,
            0.0,
        )

    def get_sources(
        self,
        keyword: str,
    ) -> list[str]:

        return self.sources.get(
            keyword,
            [],
        )