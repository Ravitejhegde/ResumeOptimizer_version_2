from docx.section import _Header

from app.services.document.models.header_model import (
    HeaderModel,
)

from app.services.document.parser.paragraph_parser import (
    ParagraphParser,
)


class HeaderParser:
    """
    Parses document headers.
    """

    @classmethod
    def parse(
        cls,
        header: _Header,
    ) -> HeaderModel:

        model = HeaderModel()

        model.paragraphs = ParagraphParser.parse(
            header.paragraphs
        )

        return model