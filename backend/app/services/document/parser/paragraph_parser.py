from docx.text.paragraph import Paragraph

from app.services.document.models.paragraph_model import (
    ParagraphModel,
)
from app.services.document.locker.run_locker import (
    RunLocker,
)
from app.services.document.parser.run_parser import (
    RunParser,
)

from app.services.hyperlink.parser.hyperlink_parser import (
    HyperlinkParser,
)
from app.services.hyperlink.parser.hyperlink_parser import (
    HyperlinkParser,
)


class ParagraphParser:
    """
    Parses Word paragraphs into ParagraphModel.
    """

    @classmethod
    def parse(
        cls,
        paragraphs: list[Paragraph],
    ) -> list[ParagraphModel]:

        result = []

        for index, paragraph in enumerate(paragraphs):

            model = ParagraphModel()

            # -----------------------------------------
            # Identity
            # -----------------------------------------

            model.id = index

            model.text = paragraph.text

            model.style = (
                paragraph.style.name
                if paragraph.style
                else ""
            )

            # -----------------------------------------
            # Paragraph Formatting
            # -----------------------------------------

            fmt = paragraph.paragraph_format

            model.alignment = (
                str(paragraph.alignment)
                if paragraph.alignment
                else "LEFT"
            )

            model.left_indent = (
                fmt.left_indent.pt
                if fmt.left_indent
                else 0
            )

            model.right_indent = (
                fmt.right_indent.pt
                if fmt.right_indent
                else 0
            )

            model.first_line_indent = (
                fmt.first_line_indent.pt
                if fmt.first_line_indent
                else 0
            )

            model.line_spacing = (
                float(fmt.line_spacing)
                if fmt.line_spacing
                else 1.0
            )

            model.spacing_before = (
                fmt.space_before.pt
                if fmt.space_before
                else 0
            )

            model.spacing_after = (
                fmt.space_after.pt
                if fmt.space_after
                else 0
            )

            model.keep_together = bool(
                fmt.keep_together
            )

            model.keep_with_next = bool(
                fmt.keep_with_next
            )

            model.page_break_before = bool(
                fmt.page_break_before
            )

            model.widow_control = bool(
                fmt.widow_control
            )

            # -----------------------------------------
            # Runs
            # -----------------------------------------

            model.runs = RunParser.parse(
                paragraph.runs
            )

            # -----------------------------------------
            # Hyperlinks
            # -----------------------------------------

            model.hyperlinks = HyperlinkParser.parse(
    paragraph
)
            # -----------------------------------------
# Lock non-editable runs
# -----------------------------------------

            RunLocker.lock(
    paragraph=paragraph,
    runs=model.runs,
    hyperlinks=model.hyperlinks,
)

            result.append(model)

        return result