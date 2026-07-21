from docx.document import Document as DocxDocument
from docx.text.paragraph import Paragraph


class ParagraphMapper:
    """
    Maps document paragraphs by index.

    Later this will support:
    - Heading mapping
    - Similarity matching
    - Block IDs
    """

    @classmethod
    def map(
        cls,
        document: DocxDocument,
    ) -> dict[int, Paragraph]:

        return {

            index: paragraph

            for index, paragraph in enumerate(
                document.paragraphs
            )

        }

    @classmethod
    def get(
        cls,
        document: DocxDocument,
        index: int,
    ) -> Paragraph | None:

        mapping = cls.map(document)

        return mapping.get(index)