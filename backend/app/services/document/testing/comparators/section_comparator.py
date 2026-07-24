from docx import Document

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class SectionComparator:
    """
    Compares document section properties.

    These properties affect page layout.
    """

    @classmethod
    def compare(
        cls,
        original: Document,
        optimized: Document,
        result: ComparisonResult,
    ):

        result.add(
            "Section Count",
            len(original.sections),
            len(optimized.sections),
        )

        count = min(
            len(original.sections),
            len(optimized.sections),
        )

        for index in range(count):

            left = original.sections[index]
            right = optimized.sections[index]

            prefix = f"Section {index+1}"

            result.add(
                f"{prefix} Page Width",
                left.page_width,
                right.page_width,
            )

            result.add(
                f"{prefix} Page Height",
                left.page_height,
                right.page_height,
            )

            result.add(
                f"{prefix} Left Margin",
                left.left_margin,
                right.left_margin,
            )

            result.add(
                f"{prefix} Right Margin",
                left.right_margin,
                right.right_margin,
            )

            result.add(
                f"{prefix} Top Margin",
                left.top_margin,
                right.top_margin,
            )

            result.add(
                f"{prefix} Bottom Margin",
                left.bottom_margin,
                right.bottom_margin,
            )

            result.add(
                f"{prefix} Header Distance",
                left.header_distance,
                right.header_distance,
            )

            result.add(
                f"{prefix} Footer Distance",
                left.footer_distance,
                right.footer_distance,
            )

            result.add(
                f"{prefix} Orientation",
                left.orientation,
                right.orientation,
            )