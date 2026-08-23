from app.application.models.optimization_request import (
    OptimizationRequest as ApplicationOptimizationRequest,
)

from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)


RESUME = "tests/resources/sample_resume.docx"

JOB_DESCRIPTION = """
We are hiring a Python Backend Developer.

Requirements:
Python
FastAPI
REST API
Docker
Git
PostgreSQL
AWS
CI/CD

Responsibilities:
Build scalable backend APIs.
Improve performance.
Write clean code.
Deploy cloud applications.
"""

OUTPUT = "tests/resources/test_optimizer_v3_output.docx"


def test_optimizer_v3_end_to_end():

    request = ApplicationOptimizationRequest(
        resume_path=RESUME,
        job_description=JOB_DESCRIPTION,
        output_path=OUTPUT,
    )

    result = ResumeOptimizationService().optimize(
        request
    )

    assert result.success is True
    assert result.output_path == OUTPUT