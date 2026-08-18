from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.models.guest import Guest
from app.database.models.guest_resume import GuestResume
from app.database.models.guest_session import GuestSession
from app.database.session import get_db

from app.guest.schemas.guest import (
    GuestSessionRequest,
    GuestSessionResponse,
)

from app.guest.schemas.guest_usage import (
    GuestOptimizationRequest,
    GuestShareRewardRequest,
    GuestShareRewardResponse,
    GuestUsageResponse,
)

from app.guest.services.guest_service import (
    GuestService,
)

from app.guest.services.guest_usage_service import (
    GuestUsageService,
)

from app.guest.services.guest_optimization_service import (
    GuestOptimizationService,
)


router = APIRouter(
    prefix="/guest",
    tags=["Guest"],
)


# ==========================================================
# Guest Session
# ==========================================================


@router.post(
    "/session",
    response_model=GuestSessionResponse,
)
def create_guest_session(
    payload: GuestSessionRequest,
    db: Session = Depends(get_db),
):
    """
    Create or retrieve an anonymous guest session.

    If a referral code is supplied, associate the
    new guest with the referrer.
    """

    service = GuestService(db)

    try:
        guest, session = service.create_or_get_session(
            browser_id=payload.browser_id,
            country=payload.country,
            language=payload.language,
            referral_code=payload.referral_code,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return GuestSessionResponse(
        guest_id=guest.id,
        session_token=session.session_token,
        country=session.country,
        language=session.language,
    )
# ==========================================================
# Guest Usage
# ==========================================================


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


# ==========================================================
# Share Reward
# ==========================================================


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


# ==========================================================
# Guest Resume Optimization
# ==========================================================


@router.post(
    "/optimize",
)
def optimize_guest_resume(
    payload: GuestOptimizationRequest,
    db: Session = Depends(get_db),
):
    """
    Optimize a guest resume using the existing
    ResumeOptimizationService.

    This route is responsible only for:

        1. Finding the guest session.
        2. Finding the guest.
        3. Verifying guest ownership of the resume.
        4. Delegating guest rules to GuestOptimizationService.

    The actual resume optimization is NOT implemented here.
    """

    # ------------------------------------------------------
    # 1. Find active guest session
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # 2. Find guest
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # 3. Find guest resume
    #
    # IMPORTANT:
    # guest_id is part of the query.
    #
    # This prevents Guest A from accessing
    # Guest B's resume.
    # ------------------------------------------------------

    guest_resume = (
        db.query(GuestResume)
        .filter(
            GuestResume.id == payload.resume_id,
            GuestResume.guest_id == guest.id,
        )
        .first()
    )

    if guest_resume is None:
        raise HTTPException(
            status_code=404,
            detail="Guest resume not found.",
        )

    # ------------------------------------------------------
    # 4. Delegate business logic
    # ------------------------------------------------------

    service = GuestOptimizationService(db)

    try:
        result = service.optimize(
            guest=guest,
            guest_resume=guest_resume,
            guest_session_id=session.id,
            job_description=payload.job_description,
        )
        return {
            "success": result.success,
            "message": result.message,
            "output_path": result.output_path,
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc