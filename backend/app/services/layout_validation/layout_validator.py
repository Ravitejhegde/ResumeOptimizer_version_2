from .paragraph_comparator import ParagraphComparator
from .validation_report import ValidationReport


class LayoutValidator:

    @staticmethod
    def validate(
        original_blocks,
        optimized_blocks,
    ) -> ValidationReport:

        report = ValidationReport()

        total_similarity = 0.0

        total = min(
            len(original_blocks),
            len(optimized_blocks),
        )

        if total == 0:
            return report

        for original, optimized in zip(
            original_blocks,
            optimized_blocks,
        ):

            result = ParagraphComparator.compare(
                paragraph_index=original.paragraph_index,
                original_text=original.text,
                optimized_text=optimized.text,
            )

            report.paragraphs.append(result)

            total_similarity += result.similarity

        report.overall_similarity = round(
            total_similarity / total,
            2,
        )

        report.passed = (
            report.overall_similarity >= 95
        )

        return report