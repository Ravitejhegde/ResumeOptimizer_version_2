from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.guest.services.guest_service import GuestService
from app.database.models.guest import Guest
from app.database.models.referral import Referral


def test_new_guest_with_referral_code_creates_referral(
    db_session: Session,
) -> None:

    referrer = Guest(
        browser_id="browser-referrer",
        country="IN",
        language="en",
    )

    db_session.add(referrer)
    db_session.commit()
    db_session.refresh(referrer)

    service = GuestService(db_session)

    referred, session = service.create_or_get_session(
        browser_id="browser-referred",
        country="IN",
        language="en",
        referral_code=referrer.referral_code,
    )

    referral = (
        db_session.query(Referral)
        .filter(
            Referral.referred_guest_id
            == referred.id,
        )
        .first()
    )

    assert referral is not None
    assert referral.referrer_guest_id == referrer.id
    assert referral.referred_guest_id == referred.id
    assert referral.status == "pending"
    assert referral.reward_granted is False

    assert session.guest_id == referred.id


def test_invalid_referral_code_is_rejected(
    db_session: Session,
) -> None:

    service = GuestService(db_session)

    with pytest.raises(
        ValueError,
        match="Referral code not found",
    ):
        service.create_or_get_session(
            browser_id="browser-new",
            country="IN",
            language="en",
            referral_code="invalid-referral-code",
        )


def test_existing_guest_does_not_create_duplicate_referral(
    db_session: Session,
) -> None:

    referrer = Guest(
        browser_id="browser-referrer",
        country="IN",
        language="en",
    )

    referred = Guest(
        browser_id="browser-referred",
        country="IN",
        language="en",
    )

    db_session.add_all(
        [
            referrer,
            referred,
        ]
    )
    db_session.commit()
    db_session.refresh(referrer)
    db_session.refresh(referred)

    service = GuestService(db_session)

    service.referral_service.create_referral(
        referrer=referrer,
        referred=referred,
    )

    service.create_or_get_session(
        browser_id=referred.browser_id,
        country="IN",
        language="en",
        referral_code=referrer.referral_code,
    )

    referrals = (
        db_session.query(Referral)
        .filter(
            Referral.referred_guest_id
            == referred.id,
        )
        .all()
    )

    assert len(referrals) == 1