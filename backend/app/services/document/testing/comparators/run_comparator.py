from docx.text.paragraph import Paragraph

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class RunComparator:
    """
    Compares all runs inside a paragraph.
    """

    @classmethod
    def compare(
        cls,
        original: Paragraph,
        optimized: Paragraph,
        result: ComparisonResult,
    ):

        result.add(
            "Run Count",
            len(original.runs),
            len(optimized.runs),
        )

        count = min(
            len(original.runs),
            len(optimized.runs),
        )

        for index in range(count):

            left = original.runs[index]
            right = optimized.runs[index]

            prefix = f"Run {index+1}"

            result.add(
                f"{prefix} Bold",
                left.bold,
                right.bold,
            )

            result.add(
                f"{prefix} Italic",
                left.italic,
                right.italic,
            )

            result.add(
                f"{prefix} Underline",
                left.underline,
                right.underline,
            )

            result.add(
                f"{prefix} Font Name",
                left.font.name,
                right.font.name,
            )

            result.add(
                f"{prefix} Font Size",
                left.font.size,
                right.font.size,
            )

            result.add(
                f"{prefix} Font Color",
                str(left.font.color.rgb),
                str(right.font.color.rgb),
            )