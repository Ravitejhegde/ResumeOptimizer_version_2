from .paragraph_comparator import (
    ParagraphComparator,
)

from .validation_report import (
    ValidationReport,
)


class LayoutValidator:
    """
    Compares the original and optimized document layouts.

    Produces an overall layout similarity score and
    a paragraph-by-paragraph validation report.
    """

    @staticmethod
    def validate(
        original_blocks,
        optimized_blocks,
    ) -> ValidationReport:

        report = ValidationReport()

        # -----------------------------------------
        # Basic Counts
        # -----------------------------------------

        report.original_paragraphs = len(
            original_blocks
        )

        report.optimized_paragraphs = len(
            optimized_blocks
        )

        total = min(
            report.original_paragraphs,
            report.optimized_paragraphs,
        )

        if total == 0:

            report.overall_similarity = 0.0
            report.passed = False

            return report

        # -----------------------------------------
        # Paragraph Comparison
        # -----------------------------------------

        total_similarity = 0.0

        for original, optimized in zip(
            original_blocks,
            optimized_blocks,
        ):

            result = ParagraphComparator.compare(

                paragraph_index=original.paragraph_index,

                original_text=original.text,

                optimized_text=optimized.text,

            )

            report.paragraphs.append(
                result
            )

            total_similarity += (
                result.similarity
            )

        # -----------------------------------------
        # Overall Similarity
        # -----------------------------------------

        report.overall_similarity = round(
            total_similarity / total,
            2,
        )

        # -----------------------------------------
        # Layout Checks
        # -----------------------------------------

        report.paragraph_count_match = (
            report.original_paragraphs
            == report.optimized_paragraphs
        )

        report.structure_match = (
            abs(
                report.original_paragraphs
                - report.optimized_paragraphs
            )
            <= 1
        )

        # -----------------------------------------
        # Pass / Fail
        # -----------------------------------------

        report.passed = (

            report.overall_similarity >= 95

            and report.structure_match

        )

        return report