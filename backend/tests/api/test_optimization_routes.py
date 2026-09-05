from __future__ import annotations

from pathlib import Path
import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies.current_user import get_current_user
from app.api.routes.optimization import router
from app.application.models.optimization_request import OptimizationRequest
from app.application.models.optimization_response import OptimizationResponse
from app.database.models.resume import Resume
from app.database.models.user import User
from app.database.models.workspace import Workspace
from app.database.session import get_db


def create_app(db, current_user: User) -> FastAPI:
    app = FastAPI()

    def override_get_db():
        yield db

    def override_get_current_user():
        return current_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    app.include_router(router)

    return app


def create_user(db, email: str) -> User:
    user = User(
        email=email,
        password_hash="test-password-hash",
        name="Optimization Test User",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_workspace(db, user: User) -> Workspace:
    workspace = Workspace(
        id=str(uuid.uuid4()),
        user_id=user.id,
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace


def create_resume(
    db,
    workspace: Workspace,
    file_path: str,
) -> Resume:
    resume = Resume(
        workspace_id=workspace.id,
        original_filename="resume.docx",
        stored_filename=f"{uuid.uuid4()}.docx",
        file_path=file_path,
        file_size=100,
        status="uploaded",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def test_optimization_route_passes_selected_skills_to_service(
    db,
    tmp_path: Path,
    monkeypatch,
):
    user = create_user(
        db,
        f"optimization-{uuid.uuid4()}@example.com",
    )
    workspace = create_workspace(db, user)

    resume_path = tmp_path / "resume.docx"
    source_resume = Path("tests/resources/sample_resume.docx")
    resume_path.write_bytes(source_resume.read_bytes())

    resume = create_resume(
        db,
        workspace,
        str(resume_path),
    )

    captured_request = {}

    class FakeService:
        def optimize(self, request: OptimizationRequest):
            captured_request["request"] = request

            return OptimizationResponse(
                success=True,
                message="Optimization completed successfully.",
                output_path=str(tmp_path / "optimized.docx"),
            )

    monkeypatch.setattr(
        "app.api.routes.optimization.ResumeOptimizationService",
        FakeService,
    )

    client = TestClient(create_app(db, user))

    response = client.post(
        "/optimization/optimize",
        json={
            "resume_id": resume.id,
            "job_description": (
                "Backend Developer with Python, FastAPI, "
                "Docker and AWS experience."
            ),
            "role_id": "backend_developer",
            "selected_skills": [
                "docker",
                "aws",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Optimization completed successfully."

    optimization_request = captured_request["request"]

    assert optimization_request.resume_path == str(resume_path)
    assert optimization_request.role_id == "backend_developer"
    assert optimization_request.selected_skills == [
        "docker",
        "aws",
    ]
    assert "Backend Developer" in optimization_request.job_description


def test_optimization_route_returns_404_for_unknown_resume(
    db,
):
    user = create_user(
        db,
        f"optimization-{uuid.uuid4()}@example.com",
    )

    client = TestClient(create_app(db, user))

    response = client.post(
        "/optimization/optimize",
        json={
            "resume_id": "does-not-exist",
            "job_description": (
                "Backend Developer with Python and FastAPI experience."
            ),
            "role_id": "backend_developer",
            "selected_skills": [],
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found."


def test_optimization_route_rejects_resume_owned_by_another_user(
    db,
    tmp_path: Path,
):
    owner = create_user(
        db,
        f"owner-{uuid.uuid4()}@example.com",
    )
    current_user = create_user(
        db,
        f"current-{uuid.uuid4()}@example.com",
    )

    workspace = create_workspace(db, owner)

    resume_path = tmp_path / "resume.docx"
    source_resume = Path("tests/resources/sample_resume.docx")
    resume_path.write_bytes(source_resume.read_bytes())

    resume = create_resume(
        db,
        workspace,
        str(resume_path),
    )

    client = TestClient(
        create_app(
            db,
            current_user,
        )
    )

    response = client.post(
        "/optimization/optimize",
        json={
            "resume_id": resume.id,
            "job_description": (
                "Backend Developer with Python and FastAPI experience."
            ),
            "role_id": "backend_developer",
            "selected_skills": [],
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this resume."
    )