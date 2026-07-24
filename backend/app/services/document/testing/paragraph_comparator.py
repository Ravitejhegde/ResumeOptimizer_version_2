from docx.text.paragraph import Paragraph

from app.services.document.testing.comparison_result import (
    ComparisonResult,
)


class ParagraphComparator:
    """
    Compares formatting between two Word paragraphs.
    """

    @classmethod
    def compare(
        cls,
        original: Paragraph,
        optimized: Paragraph,
        result: ComparisonResult,
    ):

        # -----------------------------------------
        # Style
        # -----------------------------------------

        result.add(
            "Style",
            getattr(original.style, "name", ""),
            getattr(optimized.style, "name", ""),
        )

        # -----------------------------------------
        # Alignment
        # -----------------------------------------

        result.add(
            "Alignment",
            original.alignment,
            optimized.alignment,
        )

        # -----------------------------------------
        # Left Indent
        # -----------------------------------------

        result.add(
            "Left Indent",
            original.paragraph_format.left_indent,
            optimized.paragraph_format.left_indent,
        )

        # -----------------------------------------
        # Right Indent
        # -----------------------------------------

        result.add(
            "Right Indent",
            original.paragraph_format.right_indent,
            optimized.paragraph_format.right_indent,
        )

        # -----------------------------------------
        # First Line Indent
        # -----------------------------------------

        result.add(
            "First Line Indent",
            original.paragraph_format.first_line_indent,
            optimized.paragraph_format.first_line_indent,
        )

        # -----------------------------------------
        # Space Before
        # -----------------------------------------

        result.add(
            "Space Before",
            original.paragraph_format.space_before,
            optimized.paragraph_format.space_before,
        )

        # -----------------------------------------
        # Space After
        # -----------------------------------------

        result.add(
            "Space After",
            original.paragraph_format.space_after,
            optimized.paragraph_format.space_after,
        )

        # -----------------------------------------
        # Line Spacing
        # -----------------------------------------

        result.add(
            "Line Spacing",
            original.paragraph_format.line_spacing,
            optimized.paragraph_format.line_spacing,
        )

        # -----------------------------------------
        # Keep Together
        # -----------------------------------------

        result.add(
            "Keep Together",
            original.paragraph_format.keep_together,
            optimized.paragraph_format.keep_together,
        )

        # -----------------------------------------
        # Keep With Next
        # -----------------------------------------

        result.add(
            "Keep With Next",
            original.paragraph_format.keep_with_next,
            optimized.paragraph_format.keep_with_next,
        )

        # -----------------------------------------
        # Widow Control
        # -----------------------------------------

        result.add(
            "Widow Control",
            original.paragraph_format.widow_control,
            optimized.paragraph_format.widow_control,
        )