from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.billing.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)
from app.billing.services.checkout_service import (
    CheckoutService,
)
from app.core.security.dependencies import (
    get_current_user,
)
from app.database.models.user import User
from app.database.session import get_db


router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
)
async def create_checkout(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CheckoutResponse:
    """
    Create a subscription checkout session.

    The local order remains pending until the payment
    provider confirms the payment through a webhook.
    """

    try:
        service = CheckoutService(db)

        result = await service.create_checkout(
    user_id=current_user.id,
    email=current_user.email,
    name=current_user.name,
    plan_code=request.plan,
    country=request.country,
    interval=request.interval,
    success_url=request.success_url,
    cancel_url=request.cancel_url,
    provider=request.provider,
)

        return CheckoutResponse(
            **result,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create checkout session.",
        ) from exc