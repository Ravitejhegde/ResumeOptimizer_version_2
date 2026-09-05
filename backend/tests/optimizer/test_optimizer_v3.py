from pathlib import Path
from unittest.mock import patch

from docx import Document

from app.application.models.optimization_request import (
    OptimizationRequest as ApplicationOptimizationRequest,
)
from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
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

    fake_response = """
{
    "paragraph_updates": [
        {
            "paragraph_id": "p31",
            "section": "Tools & Platforms",
            "original_text": "Tools & Platforms: Git, GitHub, Streamlit, Firebase, Postman",
            "optimized_text": "Tools & Platforms: Git, GitHub, Docker, Streamlit, Firebase, Postman",
            "confidence": 0.95,
            "reason": "Added user-selected skill Docker.",
            "approved": true,
            "formatting_safe": true
        }
    ]
}
"""

    with patch(
        "app.optimizer.engine.optimizer_engine.AIClient.optimize",
        return_value=fake_response,
    ):
        result = ResumeOptimizationService().optimize(
            request
        )

    assert result.success is True
    assert result.output_path == OUTPUT
    assert output_path.exists()

    output_document = Document(OUTPUT)

    assert (
        output_document.paragraphs[31].text
        == "Tools & Platforms: Git, GitHub, Docker, Streamlit, Firebase, Postman"
    )


def test_optimizer_failure_propagates_to_application():

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

    failed_result = OptimizationResult(
        document=None,
        paragraph_updates=[],
        warnings=["AI response validation failed."],
        success=False,
        message="AI response validation failed.",
    )

    with patch(
        "app.application.workflows.optimization_workflow.Optimizer.optimize",
        return_value=failed_result,
    ):
        result = ResumeOptimizationService().optimize(
            request
        )

    assert result.success is False
    assert result.output_path == ""
    assert not output_path.exists()