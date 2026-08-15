from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_resume import GuestResume
from app.database.models.guest_session import GuestSession
from app.database.models.usage_event import UsageEvent


# ============================================================
# Helpers
# ============================================================


def create_guest(
    db: Session,
    browser_id: str,
) -> Guest:
    guest = Guest(
        browser_id=browser_id,
        country="IN",
        language="en",
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest


def create_session(
    db: Session,
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


# ============================================================
# Guest Session
# ============================================================


def test_create_guest_session(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/guest/session",
        json={
            "browser_id": "route-browser-1",
            "country": "IN",
            "language": "en",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "guest_id" in data
    assert "session_token" in data
    assert data["country"] == "IN"
    assert data["language"] == "en"

    guest = (
        db_session.query(Guest)
        .filter(
            Guest.browser_id == "route-browser-1",
        )
        .first()
    )

    assert guest is not None
    assert guest.id == data["guest_id"]


def test_existing_guest_gets_new_session(
    client: TestClient,
    db_session: Session,
) -> None:
    first_response = client.post(
        "/guest/session",
        json={
            "browser_id": "route-browser-existing",
            "country": "IN",
            "language": "en",
        },
    )

    assert first_response.status_code == 200

    first_data = first_response.json()

    second_response = client.post(
        "/guest/session",
        json={
            "browser_id": "route-browser-existing",
            "country": "IN",
            "language": "en",
        },
    )

    assert second_response.status_code == 200

    second_data = second_response.json()

    assert (
        second_data["guest_id"]
        == first_data["guest_id"]
    )

    assert (
        second_data["session_token"]
        != first_data["session_token"]
    )

    guests = (
        db_session.query(Guest)
        .filter(
            Guest.browser_id
            == "route-browser-existing",
        )
        .all()
    )

    assert len(guests) == 1


# ============================================================
# Guest Usage
# ============================================================


def test_get_guest_usage(
    client: TestClient,
    db_session: Session,
) -> None:
    session_response = client.post(
        "/guest/session",
        json={
            "browser_id": "usage-browser-1",
            "country": "IN",
            "language": "en",
        },
    )

    assert session_response.status_code == 200

    guest_id = session_response.json()["guest_id"]

    response = client.get(
        "/guest/usage",
        params={
            "browser_id": "usage-browser-1",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["is_guest"] is True
    assert data["free_samples"] == 3
    assert data["used_samples"] == 0
    assert data["earned_samples"] == 0
    assert data["remaining_samples"] == 3
    assert data["can_optimize"] is True
    assert data["share_rewards"] == 0
    assert data["max_share_rewards"] == 5

    guest = (
        db_session.query(Guest)
        .filter(
            Guest.id == guest_id,
        )
        .first()
    )

    assert guest is not None


def test_get_usage_for_unknown_guest_returns_404(
    client: TestClient,
) -> None:
    response = client.get(
        "/guest/usage",
        params={
            "browser_id": "does-not-exist",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Guest not found."


# ============================================================
# Referral Create
# ============================================================


def test_create_referral_route(
    client: TestClient,
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "route-referrer",
    )

    referred_session = create_session(
        db_session,
        create_guest(
            db_session,
            "route-referred",
        ),
    )

    response = client.post(
        "/referral/create",
        params={
            "session_token":
                referred_session.session_token,
        },
        json={
            "referral_code":
                referrer.referral_code,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert (
        data["message"]
        == "Referral created successfully."
    )


def test_create_referral_with_invalid_session_returns_404(
    client: TestClient,
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "invalid-session-referrer",
    )

    response = client.post(
        "/referral/create",
        params={
            "session_token": "invalid-session",
        },
        json={
            "referral_code":
                referrer.referral_code,
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Guest session not found."
    )


def test_create_referral_with_invalid_code_returns_404(
    client: TestClient,
    db_session: Session,
) -> None:
    guest = create_guest(
        db_session,
        "invalid-code-guest",
    )

    session = create_session(
        db_session,
        guest,
    )

    response = client.post(
        "/referral/create",
        params={
            "session_token":
                session.session_token,
        },
        json={
            "referral_code":
                "invalid-referral-code",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Referral code not found."
    )


# ============================================================
# Share Reward
# ============================================================


def test_share_reward_route(
    client: TestClient,
    db_session: Session,
) -> None:
    guest = create_guest(
        db_session,
        "share-route-guest",
    )

    session = create_session(
        db_session,
        guest,
    )

    response = client.post(
        "/guest/share-reward",
        json={
            "session_token":
                session.session_token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "Sharing reward added successfully."
    )

    assert data["reward_samples"] == 2

    usage = data["usage"]

    assert usage["is_guest"] is True
    assert usage["earned_samples"] == 2
    assert usage["share_rewards"] == 1
    assert usage["remaining_samples"] == 5


def test_share_reward_cannot_be_claimed_twice_in_same_session(
    client: TestClient,
    db_session: Session,
) -> None:
    guest = create_guest(
        db_session,
        "duplicate-share-route",
    )

    session = create_session(
        db_session,
        guest,
    )

    first_response = client.post(
        "/guest/share-reward",
        json={
            "session_token":
                session.session_token,
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/guest/share-reward",
        json={
            "session_token":
                session.session_token,
        },
    )

    assert second_response.status_code == 400

    assert (
        second_response.json()["detail"]
        == "Share reward already claimed for this session."
    )


def test_share_reward_with_invalid_session_returns_404(
    client: TestClient,
) -> None:
    response = client.post(
        "/guest/share-reward",
        json={
            "session_token":
                "invalid-share-session",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Guest session not found."
    )


# ============================================================
# Referral + Guest Usage Integration
# ============================================================


def test_referral_and_guest_usage_work_together(
    client: TestClient,
    db_session: Session,
) -> None:
    referrer_response = client.post(
        "/guest/session",
        json={
            "browser_id":
                "integration-referrer",
            "country": "IN",
            "language": "en",
        },
    )

    assert referrer_response.status_code == 200

    referrer_data = referrer_response.json()

    referrer = (
        db_session.query(Guest)
        .filter(
            Guest.id
            == referrer_data["guest_id"],
        )
        .first()
    )

    assert referrer is not None

    referred_response = client.post(
        "/guest/session",
        json={
            "browser_id":
                "integration-referred",
            "country": "IN",
            "language": "en",
        },
    )

    assert referred_response.status_code == 200

    referred_data = referred_response.json()

    response = client.post(
        "/referral/create",
        params={
            "session_token":
                referred_data["session_token"],
        },
        json={
            "referral_code":
                referrer.referral_code,
        },
    )

    assert response.status_code == 200

    usage_response = client.get(
        "/guest/usage",
        params={
            "browser_id":
                "integration-referred",
        },
    )

    assert usage_response.status_code == 200

    usage = usage_response.json()

    assert usage["is_guest"] is True
    assert usage["remaining_samples"] == 3