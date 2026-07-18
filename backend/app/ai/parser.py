from docx import Document

from .models import ParsedResume
from .models import ResumeSection

from .section_parser import split_sections



class ResumeParser:

    def parse(self, path: str):

        document = Document(path)

        text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text.append(paragraph.text)

        sections = split_sections(
            "\n".join(text)
        )

        parsed = []

        for title, content in sections:

            parsed.append(

                ResumeSection(

                    title=title,

                    content=content,

                )

            )

        return ParsedResume(

            sections=parsed

        )