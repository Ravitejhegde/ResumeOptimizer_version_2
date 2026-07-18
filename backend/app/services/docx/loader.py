from pathlib import Path

from docx import Document


class DocxLoader:

    @staticmethod
    def load(path: str | Path) -> Document:

        path = Path(path)

        if not path.exists():

            raise FileNotFoundError(

                f"Document not found: {path}"

            )

        return Document(path)