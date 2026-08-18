from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.database.session import get_db

from app.referral.schemas.referral import (
    ReferralCreateRequest,
    ReferralCreateResponse,
)

from app.referral.services.referral_service import ReferralService


router = APIRouter(
    prefix="/referral",
    tags=["Referral"],
)


@router.post(
    "/create",
    response_model=ReferralCreateResponse,
)
def create_referral(
    payload: ReferralCreateRequest,
    session_token: str,
    db: Session = Depends(get_db),
) -> ReferralCreateResponse:
    """
    Create a referral relationship for the guest
    represented by the supplied session.
    """

    # ==========================================================
    # 1. Find active session
    # ==========================================================

    session = (
        db.query(GuestSession)
        .filter(
            GuestSession.session_token == session_token,
            GuestSession.active.is_(True),
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Guest session not found.",
        )

    # ==========================================================
    # 2. Find referred guest
    # ==========================================================

    referred_guest = (
        db.query(Guest)
        .filter(
            Guest.id == session.guest_id,
        )
        .first()
    )

    if referred_guest is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found.",
        )

    # ==========================================================
    # 3. Find referrer from referral code
    # ==========================================================

    referrer_guest = (
        db.query(Guest)
        .filter(
            Guest.referral_code == payload.referral_code,
        )
        .first()
    )

    if referrer_guest is None:
        raise HTTPException(
            status_code=404,
            detail="Referral code not found.",
        )

    # ==========================================================
    # 4. Create referral
    # ==========================================================

    service = ReferralService(db)

    try:
        service.create_referral(
            referrer=referrer_guest,
            referred=referred_guest,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # ==========================================================
    # 5. Success
    # ==========================================================

    return ReferralCreateResponse(
        success=True,
        message="Referral created successfully.",
    )