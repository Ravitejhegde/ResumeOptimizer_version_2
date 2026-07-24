from dataclasses import dataclass, field

from .comparison_result import (
    ComparisonResult,
)


@dataclass(slots=True)
class ValidationReport:
    """
    Overall layout validation report.
    """

    # -----------------------------------------
    # Overall Score
    # -----------------------------------------

    overall_similarity: float = 0.0

    passed: bool = False

    # -----------------------------------------
    # Paragraph Counts
    # -----------------------------------------

    original_paragraphs: int = 0

    optimized_paragraphs: int = 0

    paragraph_count_match: bool = False

    structure_match: bool = False

    # -----------------------------------------
    # Paragraph Results
    # -----------------------------------------

    paragraphs: list[ComparisonResult] = field(
        default_factory=list
    )