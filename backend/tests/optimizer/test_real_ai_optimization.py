from pathlib import Path

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

OUTPUT = "tests/resources/test_real_ai_optimized.docx"


def test_real_ai_optimization():
    output_path = Path(OUTPUT)

    if output_path.exists():
        output_path.unlink()

    request = ApplicationOptimizationRequest(
        resume_path=RESUME,
        job_description=JOB_DESCRIPTION,
        output_path=OUTPUT,
        role_id="backend_developer",
        selected_skills=["Docker"],
    )

    result = ResumeOptimizationService().optimize(request)

    print("\n========== REAL AI RESULT ==========")
    print("Success:", result.success)
    print("Message:", result.message)
    print("Output:", result.output_path)
    print("====================================\n")

    assert result.success is True
    assert result.output_path
    assert Path(result.output_path).exists()