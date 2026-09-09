from pathlib import Path

from app.application.models.optimization_request import (
    OptimizationRequest as ApplicationOptimizationRequest,
)
from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)


RESUME = "tests/resources/sample_resume.docx"

JOB_DESCRIPTION = """
FULL STACK DEVELOPER

We are looking for a Full Stack Developer to design, develop,
test, deploy, and maintain modern web applications.

REQUIRED SKILLS

Frontend:
React
JavaScript
TypeScript
HTML
CSS

Backend:
Python
FastAPI
REST API
Node.js
Express

Database:
SQL
PostgreSQL
MongoDB

Tools and Platforms:
Git
GitHub
Docker
AWS

Development Practices:
API integration
Authentication
Testing
CI/CD
Agile development

RESPONSIBILITIES

Build responsive and maintainable web applications.

Develop frontend interfaces using React, JavaScript,
and TypeScript.

Develop backend services and REST APIs using Python,
FastAPI, Node.js, and Express.

Design and integrate SQL and NoSQL databases.

Integrate frontend applications with backend APIs.

Implement authentication and secure application flows.

Write clean, reusable, maintainable, and testable code.

Debug application issues and improve reliability.

Use Git and GitHub for source control and collaboration.

Containerize applications using Docker.

Deploy and maintain applications in cloud environments
such as AWS.

Participate in CI/CD and Agile development practices.

Work across the complete software development lifecycle.

PREFERRED QUALIFICATIONS

Experience building full-stack web applications.

Experience with React and TypeScript.

Experience developing RESTful APIs.

Experience with PostgreSQL or MongoDB.

Experience with Docker and AWS.

Strong problem-solving and communication skills.
"""

OUTPUT = "tests/resources/test_real_ai_fullstack_optimized.docx"


def test_real_ai_fullstack_optimization():
    output_path = Path(OUTPUT)

    if output_path.exists():
        output_path.unlink()

    request = ApplicationOptimizationRequest(
        resume_path=RESUME,
        job_description=JOB_DESCRIPTION,
        output_path=OUTPUT,
        role_id="full_stack_developer",
        selected_skills=[
            "React",
            "JavaScript",
            "TypeScript",
            "Docker",
            "AWS",
        ],
    )

    result = ResumeOptimizationService().optimize(request)

    print("\n========== REAL AI FULL STACK RESULT ==========")
    print("Success:", result.success)
    print("Message:", result.message)
    print("Output:", result.output_path)
    print("===============================================\n")

    assert result.success is True
    assert result.output_path
    assert Path(result.output_path).exists()