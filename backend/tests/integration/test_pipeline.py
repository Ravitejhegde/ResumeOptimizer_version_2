from pathlib import Path

from app.services.pipeline.optimization_pipeline import (
    OptimizationPipeline,
)


BASE_DIR = Path(__file__).parent

SAMPLES = (
    BASE_DIR.parent
    / "document"
    / "samples"
)

OUTPUT = (
    BASE_DIR
    / "output"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True,
)

INPUT_FILE = (
    SAMPLES
    / "sample_resume.docx"
)

OUTPUT_FILE = (
    OUTPUT
    / "optimized_resume.docx"
)


JOB_DESCRIPTION = """
We are hiring a Python Backend Developer.

Requirements

- Python
- FastAPI
- REST API
- Docker
- Git
- PostgreSQL
- AWS
- CI/CD

Responsibilities

- Build scalable backend APIs

- Improve performance

- Write clean code

- Deploy cloud applications
"""


def main():

    print()

    print("=" * 70)

    print("RESUME OPTIMIZER V3")

    print("=" * 70)

    result = OptimizationPipeline.optimize(

        input_file=str(INPUT_FILE),

        job_description=JOB_DESCRIPTION,

        output_file=str(OUTPUT_FILE),

    )

    print()

    print("=" * 70)

    print("PIPELINE COMPLETED")

    print("=" * 70)

    print()

    print("Role")

    print(result["role"])

    print()

    print("Output")

    print(result["output"])

    print()

    print("=" * 70)


if __name__ == "__main__":

    main()