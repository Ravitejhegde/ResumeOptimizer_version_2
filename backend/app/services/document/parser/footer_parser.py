from docx.section import _Footer

from app.services.document.models.footer_model import (
    FooterModel,
)

from app.services.document.parser.paragraph_parser import (
    ParagraphParser,
)


class FooterParser:
    """
    Parses document footers.
    """

    @classmethod
    def parse(
        cls,
        footer: _Footer,
    ) -> FooterModel:

        model = FooterModel()

        model.paragraphs = ParagraphParser.parse(
            footer.paragraphs
        )

        return model