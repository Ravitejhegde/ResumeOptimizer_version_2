from __future__ import annotations

from pathlib import Path
import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.analysis import router
from app.database.models.resume import Resume
from app.database.models.workspace import Workspace
from app.database.session import get_db


def create_app(db) -> FastAPI:
    app = FastAPI()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    app.include_router(router)

    return app


def create_workspace(db) -> Workspace:
    from app.database.models.user import User

    user = User(
        email=f"analysis-{uuid.uuid4()}@example.com",
        password_hash="test-password-hash",
        name="Analysis Test User",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

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


def test_analysis_match_returns_match_result(
    db,
    tmp_path: Path,
):
    workspace = create_workspace(db)

    resume_path = tmp_path / "resume.docx"

    source_resume = Path(
        "tests/resources/sample_resume.docx"
    )

    resume_path.write_bytes(
        source_resume.read_bytes()
    )

    resume = create_resume(
        db,
        workspace,
        str(resume_path),
    )

    client = TestClient(
        create_app(db)
    )

    response = client.post(
        "/analysis/match",
        json={
            "resume_id": resume.id,
            "job_description": (
                "Python developer with "
                "FastAPI experience."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "score" in data
    assert "matched_skills" in data
    assert "missing_skills" in data
    assert "extra_skills" in data

    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 100
    assert isinstance(data["matched_skills"], list)
    assert isinstance(data["missing_skills"], list)
    assert isinstance(data["extra_skills"], list)


def test_analysis_match_requires_job_description(
    db,
    tmp_path: Path,
):
    workspace = create_workspace(db)

    resume_path = tmp_path / "resume.docx"

    source_resume = Path(
        "tests/resources/sample_resume.docx"
    )

    resume_path.write_bytes(
        source_resume.read_bytes()
    )

    resume = create_resume(
        db,
        workspace,
        str(resume_path),
    )

    client = TestClient(
        create_app(db)
    )

    response = client.post(
        "/analysis/match",
        json={
            "resume_id": resume.id,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Job description is required "
        "for match analysis."
    )


def test_analysis_match_returns_404_for_unknown_resume(
    db,
):
    client = TestClient(
        create_app(db)
    )

    response = client.post(
        "/analysis/match",
        json={
            "resume_id": "does-not-exist",
            "job_description": (
                "Python developer with "
                "FastAPI experience."
            ),
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Resume not found."
    )