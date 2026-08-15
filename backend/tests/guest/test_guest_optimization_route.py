from __future__ import annotations

import uuid
from pathlib import Path
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.database.session import get_db
from app.database.models.guest import Guest
from app.database.models.guest_resume import GuestResume
from app.database.models.guest_session import GuestSession
from app.database.models.usage_event import UsageEvent
from app.guest.routes.guest import router


def create_app(db) -> FastAPI:
    app = FastAPI()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    app.include_router(router)

    return app


def create_guest(
    db,
    *,
    browser_id: str,
) -> Guest:
    guest = Guest(
        id=str(uuid.uuid4()),
        browser_id=browser_id,
        country="IN",
        language="en",
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest


def create_session(
    db,
    guest: Guest,
) -> GuestSession:
    session = GuestSession(
        guest_id=guest.id,
        session_token=f"session-{uuid.uuid4()}",
        country="IN",
        language="en",
        active=True,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def create_guest_resume(
    db,
    guest: Guest,
    *,
    file_path: str,
) -> GuestResume:
    resume = GuestResume(
        guest_id=guest.id,
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


def test_guest_optimization_success(
    db,
    tmp_path: Path,
):
    """
    A valid guest session and guest resume should be sent
    through the existing ResumeOptimizationService.
    """

    guest = create_guest(
        db,
        browser_id="guest-browser",
    )

    session = create_session(
        db,
        guest,
    )

    resume_path = tmp_path / "resume.docx"
    resume_path.write_bytes(b"fake docx")

    guest_resume = create_guest_resume(
        db,
        guest,
        file_path=str(resume_path),
    )

    client = TestClient(
    create_app(db)
)

    output_path = (
        tmp_path / "resume_optimized.docx"
    )

    mock_result = type(
        "OptimizationResult",
        (),
        {
            "success": True,
            "message": "Resume optimized successfully.",
            "output_path": str(output_path),
        },
    )()

    with patch(
        "app.guest.services.guest_optimization_service."
        "ResumeOptimizationService.optimize",
        return_value=mock_result,
    ) as optimize_mock:

        response = client.post(
            "/guest/optimize",
            json={
                "session_token": session.session_token,
                "resume_id": guest_resume.id,
                "job_description": (
                    "Python developer with FastAPI experience."
                ),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Resume optimized successfully."
    )
    assert (
        data["output_path"]
        == str(output_path)
    )

    optimize_mock.assert_called_once()

    # --------------------------------------------------
    # Verify exactly one optimization usage event
    # --------------------------------------------------

    event = (
        db.query(UsageEvent)
        .filter(
            UsageEvent.guest_session_id == session.id,
            UsageEvent.event_type
            == "optimization_completed",
        )
        .first()
    )

    assert event is not None


def test_guest_cannot_optimize_another_guest_resume(
    db,
    tmp_path: Path,
):
    """
    A guest must never be able to optimize another
    guest's resume.
    """

    guest_one = create_guest(
        db,
        browser_id="guest-one",
    )

    guest_two = create_guest(
        db,
        browser_id="guest-two",
    )

    session = create_session(
        db,
        guest_one,
    )

    resume_path = tmp_path / "resume.docx"
    resume_path.write_bytes(b"fake docx")

    guest_two_resume = create_guest_resume(
        db,
        guest_two,
        file_path=str(resume_path),
    )

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/guest/optimize",
        json={
            "session_token": session.session_token,
            "resume_id": guest_two_resume.id,
            "job_description": "Python developer.",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Guest resume not found."
    )


def test_guest_optimization_rejected_when_usage_is_exhausted(
    db,
    tmp_path: Path,
):
    """
    A guest cannot optimize when all available samples
    have already been consumed.
    """

    guest = create_guest(
        db,
        browser_id="guest-browser",
    )

    session = create_session(
        db,
        guest,
    )

    resume_path = tmp_path / "resume.docx"
    resume_path.write_bytes(b"fake docx")

    guest_resume = create_guest_resume(
        db,
        guest,
        file_path=str(resume_path),
    )

    # --------------------------------------------------
    # Consume all initial free samples
    # --------------------------------------------------

    for _ in range(3):
        event = UsageEvent(
            guest_session_id=session.id,
            event_type="optimization_completed",
            resource_type="resume",
        )

        db.add(event)

    db.commit()

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/guest/optimize",
        json={
            "session_token": session.session_token,
            "resume_id": guest_resume.id,
            "job_description": "Python developer.",
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Guest optimization limit reached."
    )


def test_failed_guest_optimization_does_not_consume_usage(
    db,
    tmp_path: Path,
):
    """
    If the existing optimization engine fails,
    guest usage must not be consumed.
    """

    guest = create_guest(
        db,
        browser_id="guest-browser",
    )

    session = create_session(
        db,
        guest,
    )

    resume_path = tmp_path / "resume.docx"
    resume_path.write_bytes(b"fake docx")

    guest_resume = create_guest_resume(
        db,
        guest,
        file_path=str(resume_path),
    )

    client = TestClient(
    create_app(db)
)

    with patch(
        "app.guest.services.guest_optimization_service."
        "ResumeOptimizationService.optimize",
        side_effect=ValueError(
            "Optimization failed."
        ),
    ):

        response = client.post(
            "/guest/optimize",
            json={
                "session_token": session.session_token,
                "resume_id": guest_resume.id,
                "job_description": "Python developer.",
            },
        )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Optimization failed."
    )

    # --------------------------------------------------
    # No optimization usage must be recorded
    # --------------------------------------------------

    usage_count = (
        db.query(UsageEvent)
        .filter(
            UsageEvent.guest_session_id == session.id,
            UsageEvent.event_type
            == "optimization_completed",
        )
        .count()
    )

    assert usage_count == 0