from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.referral.services.referral_service import ReferralService


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


# ============================================================
# Create Referral
# ============================================================


def test_create_referral(
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "browser-referrer",
    )

    referred = create_guest(
        db_session,
        "browser-referred",
    )

    service = ReferralService(db_session)

    referral = service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    assert referral.referrer_guest_id == referrer.id
    assert referral.referred_guest_id == referred.id
    assert referral.status == "pending"
    assert referral.reward_granted is False
    assert referral.rewarded_at is None


# ============================================================
# Self Referral
# ============================================================


def test_guest_cannot_refer_themselves(
    db_session: Session,
) -> None:
    guest = create_guest(
        db_session,
        "browser-1",
    )

    service = ReferralService(db_session)

    with pytest.raises(
        ValueError,
        match="cannot refer themselves",
    ):
        service.create_referral(
            referrer=guest,
            referred=guest,
        )


# ============================================================
# One Referrer Per Guest
# ============================================================


def test_referred_guest_cannot_have_two_referrers(
    db_session: Session,
) -> None:
    referrer_one = create_guest(
        db_session,
        "browser-1",
    )

    referrer_two = create_guest(
        db_session,
        "browser-2",
    )

    referred = create_guest(
        db_session,
        "browser-3",
    )

    service = ReferralService(db_session)

    service.create_referral(
        referrer=referrer_one,
        referred=referred,
    )

    with pytest.raises(
        ValueError,
        match="already been referred",
    ):
        service.create_referral(
            referrer=referrer_two,
            referred=referred,
        )


# ============================================================
# Complete Referral
# ============================================================


def test_pending_referral_can_be_completed(
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "browser-1",
    )

    referred = create_guest(
        db_session,
        "browser-2",
    )

    service = ReferralService(db_session)

    referral = service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    assert referral.status == "pending"

    completed = service.complete_referral(
        referral,
    )

    assert completed.status == "completed"
    assert completed.reward_granted is False


# ============================================================
# Reward
# ============================================================


def test_completed_referral_can_be_rewarded(
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "browser-1",
    )

    referred = create_guest(
        db_session,
        "browser-2",
    )

    service = ReferralService(db_session)

    referral = service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    service.complete_referral(
        referral,
    )

    rewarded = service.grant_reward(
        referral,
    )

    assert rewarded.status == "completed"
    assert rewarded.reward_granted is True
    assert rewarded.rewarded_at is not None


# ============================================================
# Cannot Reward Pending Referral
# ============================================================


def test_pending_referral_cannot_be_rewarded(
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "browser-1",
    )

    referred = create_guest(
        db_session,
        "browser-2",
    )

    service = ReferralService(db_session)

    referral = service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    with pytest.raises(
        ValueError,
        match="not eligible for reward",
    ):
        service.grant_reward(
            referral,
        )


# ============================================================
# Duplicate Reward
# ============================================================


def test_referral_cannot_be_rewarded_twice(
    db_session: Session,
) -> None:
    referrer = create_guest(
        db_session,
        "browser-1",
    )

    referred = create_guest(
        db_session,
        "browser-2",
    )

    service = ReferralService(db_session)

    referral = service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    service.complete_referral(
        referral,
    )

    service.grant_reward(
        referral,
    )

    with pytest.raises(
        ValueError,
        match="already been granted",
    ):
        service.grant_reward(
            referral,
        )