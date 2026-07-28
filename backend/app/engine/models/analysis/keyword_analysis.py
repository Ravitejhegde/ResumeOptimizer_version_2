from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KeywordAnalysis:
    """
    Technologies extracted from the document.
    """

    detected: list[str] = field(
        default_factory=list,
    )

    normalized: list[str] = field(
        default_factory=list,
    )

    duplicates: list[str] = field(
        default_factory=list,
    )

    categories: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )
