from docx import Document


class ResumeExtractor:

    @staticmethod
    def extract(path: str) -> str:

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)