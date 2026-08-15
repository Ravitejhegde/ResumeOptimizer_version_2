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


# ==========================================================
# Create Referral
# ==========================================================


@router.post(
    "/create",
    response_model=ReferralCreateResponse,
)
def create_referral(
    payload: ReferralCreateRequest,
    session_token: str,
    db: Session = Depends(get_db),
):
    """
    Create a referral when a guest enters through
    another guest's referral code.
    """

    # ------------------------------------------------------
    # Find referred guest from current session
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Find referrer using referral code
    # ------------------------------------------------------

    referrer = (
        db.query(Guest)
        .filter(
            Guest.referral_code == payload.referral_code,
        )
        .first()
    )

    if referrer is None:
        raise HTTPException(
            status_code=404,
            detail="Referral code not found.",
        )

    # ------------------------------------------------------
    # Create referral
    # ------------------------------------------------------

    service = ReferralService(db)

    try:
        service.create_referral(
            referrer=referrer,
            referred=referred_guest,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return ReferralCreateResponse(
        success=True,
        message="Referral created successfully.",
    )