from dataclasses import dataclass


@dataclass(slots=True)
class ComparisonResult:

    paragraph_index: int

    original_lines: int

    optimized_lines: int

    line_difference: int

    original_length: int

    optimized_length: int

    similarity: float

    passed: bool