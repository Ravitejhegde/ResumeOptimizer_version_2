from dataclasses import dataclass, field

from .comparison_result import ComparisonResult


@dataclass(slots=True)
class ValidationReport:

    overall_similarity: float = 0.0

    passed: bool = False

    paragraphs: list[ComparisonResult] = field(
        default_factory=list
    )