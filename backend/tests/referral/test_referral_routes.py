from __future__ import annotations

import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.referral.routes.referral import router
from app.database.session import get_db

def create_app(db):
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


def test_create_referral_success(db):
    """
    A guest arriving through another guest's referral code
    should create a pending referral.
    """

    referrer = create_guest(
        db,
        browser_id="referrer-browser",
    )

    referred = create_guest(
        db,
        browser_id="referred-browser",
    )

    session = create_session(
        db,
        referred,
    )

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/referral/create",
        params={
            "session_token": session.session_token,
        },
        json={
            "referral_code": referrer.referral_code,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Referral created successfully."
    )


def test_create_referral_invalid_session(db):
    """
    An unknown session must be rejected.
    """

    referrer = create_guest(
        db,
        browser_id="referrer-browser",
    )

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/referral/create",
        params={
            "session_token": "invalid-session",
        },
        json={
            "referral_code": referrer.referral_code,
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Guest session not found."
    )


def test_create_referral_invalid_code(db):
    """
    An unknown referral code must be rejected.
    """

    referred = create_guest(
        db,
        browser_id="referred-browser",
    )

    session = create_session(
        db,
        referred,
    )

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/referral/create",
        params={
            "session_token": session.session_token,
        },
        json={
            "referral_code": "does-not-exist",
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Referral code not found."
    )


def test_self_referral_is_rejected(db):
    """
    A guest must not be able to refer themselves.
    """

    guest = create_guest(
        db,
        browser_id="same-browser",
    )

    session = create_session(
        db,
        guest,
    )

    client = TestClient(
    create_app(db)
)

    response = client.post(
        "/referral/create",
        params={
            "session_token": session.session_token,
        },
        json={
            "referral_code": guest.referral_code,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "A guest cannot refer themselves."
    )


def test_duplicate_referral_is_rejected(db):
    """
    The same guest cannot be referred twice.
    """

    referrer = create_guest(
        db,
        browser_id="referrer-browser",
    )

    referred = create_guest(
        db,
        browser_id="referred-browser",
    )

    session = create_session(
        db,
        referred,
    )

    client = TestClient(
    create_app(db)
)

    first = client.post(
        "/referral/create",
        params={
            "session_token": session.session_token,
        },
        json={
            "referral_code": referrer.referral_code,
        },
    )

    assert first.status_code == 200

    second = client.post(
        "/referral/create",
        params={
            "session_token": session.session_token,
        },
        json={
            "referral_code": referrer.referral_code,
        },
    )

    assert second.status_code == 400
    assert (
        second.json()["detail"]
        == "This guest has already been referred."
    )