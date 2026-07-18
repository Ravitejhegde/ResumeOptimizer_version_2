from .comparison_result import ComparisonResult


class ParagraphComparator:
    """
    Compares one original paragraph against
    one optimized paragraph.
    """

    @staticmethod
    def compare(
        paragraph_index: int,
        original_text: str,
        optimized_text: str,
    ) -> ComparisonResult:

        original_length = len(original_text)
        optimized_length = len(optimized_text)

        difference = abs(
            original_length - optimized_length
        )

        if original_length == 0:
            similarity = 100.0
        else:
            similarity = max(
                0.0,
                (
                    1
                    - difference / original_length
                )
                * 100,
            )

        return ComparisonResult(
            paragraph_index=paragraph_index,
            original_lines=1,
            optimized_lines=1,
            line_difference=0,
            original_length=original_length,
            optimized_length=optimized_length,
            similarity=round(similarity, 2),
            passed=similarity >= 95,
        )