from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_session import GuestSession
from app.database.session import get_db
from app.guest.schemas.guest import (
    GuestSessionRequest,
    GuestSessionResponse,
)
from app.guest.schemas.guest_usage import (
    GuestShareRewardRequest,
    GuestShareRewardResponse,
    GuestUsageResponse,
)
from app.guest.services.guest_service import GuestService
from app.guest.services.guest_usage_service import GuestUsageService


router = APIRouter(
    prefix="/guest",
    tags=["Guest"],
)


@router.post(
    "/session",
    response_model=GuestSessionResponse,
)
def create_guest_session(
    payload: GuestSessionRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Create or retrieve an anonymous guest session.
    """

    service = GuestService(db)

    user_agent = request.headers.get("user-agent")

    ip_address = (
        request.client.host
        if request.client
        else None
    )

    guest, session = service.create_or_get_session(
        browser_id=payload.browser_id,
        country=payload.country,
        language=payload.language,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return GuestSessionResponse(
        guest_id=guest.id,
        session_token=session.session_token,
        country=session.country,
        language=session.language,
    )


@router.get(
    "/usage",
    response_model=GuestUsageResponse,
)
def get_guest_usage(
    browser_id: str,
    db: Session = Depends(get_db),
):
    """
    Return current guest free usage.

    The browser_id identifies the anonymous guest.
    """

    guest = (
        db.query(Guest)
        .filter(
            Guest.browser_id == browser_id,
        )
        .first()
    )

    if guest is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found.",
        )

    service = GuestUsageService(db)

    return service.get_usage(guest)


@router.post(
    "/share-reward",
    response_model=GuestShareRewardResponse,
)
def claim_share_reward(
    payload: GuestShareRewardRequest,
    db: Session = Depends(get_db),
):
    """
    Claim one guest sharing reward.

    The session token identifies the guest session.
    The business rules are enforced by GuestUsageService.
    """

    session = (
        db.query(GuestSession)
        .filter(
            GuestSession.session_token
            == payload.session_token,
            GuestSession.active.is_(True),
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Guest session not found.",
        )

    guest = (
        db.query(Guest)
        .filter(
            Guest.id == session.guest_id,
        )
        .first()
    )

    if guest is None:
        raise HTTPException(
            status_code=404,
            detail="Guest not found.",
        )

    service = GuestUsageService(db)

    try:
        service.record_share_reward(
            guest=guest,
            guest_session_id=session.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    usage = service.get_usage(guest)

    return GuestShareRewardResponse(
        message="Sharing reward added successfully.",
        reward_samples=2,
        usage=usage,
    )