from docx.document import Document as DocxDocument


class ParagraphMapper:
    """
    Maps paragraph IDs to Word paragraphs.
    """

    @classmethod
    def map(
        cls,
        document: DocxDocument,
    ):

        mapping = {}

        for index, paragraph in enumerate(
            document.paragraphs,
            start=1,
        ):

            paragraph_id = f"P{index:05}"

            mapping[
                paragraph_id
            ] = paragraph

        return mapping