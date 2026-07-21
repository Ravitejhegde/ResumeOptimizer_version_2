from app.services.document.parser.document_parser import (
    DocumentParser,
)

from app.services.document.writer.document_writer import (
    DocumentWriter,
)
from pathlib import Path

BASE_DIR = Path(__file__).parent

INPUT = BASE_DIR / "samples" / "sample_resume.docx"
OUTPUT = BASE_DIR / "samples" / "sample_resume_copy.docx"


def main():

    print()

    print("=" * 60)

    print("PARSING DOCUMENT")

    print("=" * 60)

    model = DocumentParser.parse(
        INPUT
    )

    print()

    print("WRITING DOCUMENT")

    print("=" * 60)

    DocumentWriter.write(
        model,
        OUTPUT,
    )

    print()

    print("DONE")

    print()

    print(f"Input : {INPUT}")

    print(f"Output: {OUTPUT}")


if __name__ == "__main__":

    main()