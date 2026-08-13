from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.guest.schemas.guest import (
    GuestSessionRequest,
    GuestSessionResponse,
)
from app.guest.services.guest_service import GuestService
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models.guest import Guest
from app.guest.schemas.guest_usage import GuestUsageResponse
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

    service = GuestService(db)

    user_agent = request.headers.get(
        "user-agent",
    )

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