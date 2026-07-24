from app.services.parser.models import ResumeDocument


class NameExtractor:
    """
    Extracts the candidate name.

    Assumption:
    The first non-empty paragraph is the name.
    """

    @staticmethod
    def extract(
        document: ResumeDocument,
    ) -> str:

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:

                return text

        return ""