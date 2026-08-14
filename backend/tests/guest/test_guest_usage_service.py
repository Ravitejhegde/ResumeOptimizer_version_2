from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.guest.services.guest_usage_service import (
    GUEST_INITIAL_FREE_SAMPLES,
    GUEST_MAX_SHARE_REWARDS,
    GUEST_SHARE_REWARD_SAMPLES,
    GuestUsageService,
)


def create_guest(
    db: Session,
    browser_id: str = "browser-1",
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
    from secrets import token_urlsafe

    session = GuestSession(
        guest_id=guest.id,
        session_token=token_urlsafe(32),
        country="IN",
        language="en",
        active=True,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# ============================================================
# Initial Usage
# ============================================================


def test_new_guest_starts_with_three_samples(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)

    service = GuestUsageService(db_session)

    usage = service.get_usage(guest)

    assert usage["is_guest"] is True
    assert usage["free_samples"] == 3
    assert usage["used_samples"] == 0
    assert usage["earned_samples"] == 0
    assert usage["remaining_samples"] == 3
    assert usage["can_optimize"] is True
    assert usage["share_rewards"] == 0
    assert usage["max_share_rewards"] == 5


# ============================================================
# Share Reward
# ============================================================


def test_one_share_gives_two_samples(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    service = GuestUsageService(db_session)

    service.record_share_reward(
        guest=guest,
        guest_session_id=session.id,
    )

    usage = service.get_usage(guest)

    assert usage["share_rewards"] == 1
    assert usage["earned_samples"] == 2
    assert usage["remaining_samples"] == 5


def test_same_session_cannot_claim_reward_twice(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    service = GuestUsageService(db_session)

    service.record_share_reward(
        guest=guest,
        guest_session_id=session.id,
    )

    with pytest.raises(
        ValueError,
        match="already claimed",
    ):
        service.record_share_reward(
            guest=guest,
            guest_session_id=session.id,
        )


def test_different_sessions_can_claim_rewards(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)

    session_one = create_session(
        db_session,
        guest,
    )

    session_two = create_session(
        db_session,
        guest,
    )

    service = GuestUsageService(db_session)

    service.record_share_reward(
        guest=guest,
        guest_session_id=session_one.id,
    )

    service.record_share_reward(
        guest=guest,
        guest_session_id=session_two.id,
    )

    usage = service.get_usage(guest)

    assert usage["share_rewards"] == 2
    assert usage["earned_samples"] == 4
    assert usage["remaining_samples"] == 7


# ============================================================
# Maximum Rewards
# ============================================================


def test_guest_can_claim_at_most_five_rewards(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)

    service = GuestUsageService(db_session)

    sessions = [
        create_session(db_session, guest)
        for _ in range(GUEST_MAX_SHARE_REWARDS)
    ]

    for session in sessions:
        service.record_share_reward(
            guest=guest,
            guest_session_id=session.id,
        )

    usage = service.get_usage(guest)

    assert usage["share_rewards"] == 5
    assert usage["earned_samples"] == 10
    assert usage["remaining_samples"] == 13


def test_sixth_reward_is_rejected(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)

    service = GuestUsageService(db_session)

    sessions = [
        create_session(db_session, guest)
        for _ in range(6)
    ]

    for session in sessions[:5]:
        service.record_share_reward(
            guest=guest,
            guest_session_id=session.id,
        )

    with pytest.raises(
        ValueError,
        match="Maximum guest sharing rewards reached",
    ):
        service.record_share_reward(
            guest=guest,
            guest_session_id=sessions[5].id,
        )


# ============================================================
# Optimization Consumption
# ============================================================


def test_optimization_consumes_one_sample(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    service = GuestUsageService(db_session)

    service.consume_optimization(
        guest=guest,
        guest_session_id=session.id,
    )

    usage = service.get_usage(guest)

    assert usage["used_samples"] == 1
    assert usage["remaining_samples"] == 2


def test_guest_can_use_all_three_initial_samples(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    service = GuestUsageService(db_session)

    for _ in range(3):
        service.consume_optimization(
            guest=guest,
            guest_session_id=session.id,
        )

    usage = service.get_usage(guest)

    assert usage["used_samples"] == 3
    assert usage["remaining_samples"] == 0
    assert usage["can_optimize"] is False


def test_optimization_is_rejected_when_no_samples_remain(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    service = GuestUsageService(db_session)

    for _ in range(3):
        service.consume_optimization(
            guest=guest,
            guest_session_id=session.id,
        )

    with pytest.raises(
        ValueError,
        match="Guest optimization limit reached",
    ):
        service.consume_optimization(
            guest=guest,
            guest_session_id=session.id,
        )


# ============================================================
# Session Security
# ============================================================


def test_invalid_session_is_rejected(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)

    service = GuestUsageService(db_session)

    with pytest.raises(
        ValueError,
        match="Invalid guest session",
    ):
        service.record_share_reward(
            guest=guest,
            guest_session_id="invalid-session-id",
        )


def test_guest_cannot_use_another_guests_session(
    db_session: Session,
) -> None:
    guest_one = create_guest(
        db_session,
        browser_id="browser-1",
    )

    guest_two = create_guest(
        db_session,
        browser_id="browser-2",
    )

    session_one = create_session(
        db_session,
        guest_one,
    )

    service = GuestUsageService(db_session)

    with pytest.raises(
        ValueError,
        match="Invalid guest session",
    ):
        service.record_share_reward(
            guest=guest_two,
            guest_session_id=session_one.id,
        )


def test_inactive_session_is_rejected(
    db_session: Session,
) -> None:
    guest = create_guest(db_session)
    session = create_session(db_session, guest)

    session.active = False
    db_session.commit()

    service = GuestUsageService(db_session)

    with pytest.raises(
        ValueError,
        match="Invalid guest session",
    ):
        service.record_share_reward(
            guest=guest,
            guest_session_id=session.id,
        )


# ============================================================
# Configuration Consistency
# ============================================================


def test_reward_configuration_is_two_samples(
    db_session: Session,
) -> None:
    assert GUEST_INITIAL_FREE_SAMPLES == 3
    assert GUEST_SHARE_REWARD_SAMPLES == 2
    assert GUEST_MAX_SHARE_REWARDS == 5