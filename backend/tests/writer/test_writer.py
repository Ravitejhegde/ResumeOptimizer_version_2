"""
Writer integration test.
"""

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)
from app.writer.services.writer import (
    Writer,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)


SOURCE = r"tests\resources\sample_resume.docx"

OUTPUT = r"tests\output\optimized_resume.docx"


def main() -> None:

    document = DocumentAnalyzer().analyze(
        SOURCE,
    )

    optimization = OptimizationResult(
        document=document,
        success=True,
        message="Writer test",
    )

    writer = Writer()

    result = writer.write(
        source_file=SOURCE,
        output_file=OUTPUT,
        document=document,
        optimization=optimization,
    )

    print("=" * 60)
    print("WRITER RESULT")
    print("=" * 60)

    print("Success :", result.success)
    print("Output  :", result.output_path)
    print("Message :", result.message)


if __name__ == "__main__":
    main()