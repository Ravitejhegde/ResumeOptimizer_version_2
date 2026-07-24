from contextlib import redirect_stdout

from app.services.document.testing.document_comparator import (
    DocumentComparator,
)


def main():

    result = DocumentComparator.compare(
        "tests/document/samples/sample_resume.docx",
        "tests/integration/output/optimized_resume.docx",
    )

    with open(
        "tests/document/comparison_report.txt",
        "w",
        encoding="utf-8",
    ) as file:

        with redirect_stdout(file):
            result.print_report()

    print()
    print("Comparison report saved to:")
    print("tests/document/comparison_report.txt")


if __name__ == "__main__":
    main()