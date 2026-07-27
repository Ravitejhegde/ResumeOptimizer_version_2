from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.security.dependencies import (
    get_current_user,
)

from app.database.models.user import (
    User,
)

from app.database.session import (
    get_db,
)

from app.billing.services.checkout_service import (
    CheckoutService,
)

from app.billing.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
)
def create_checkout(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:

        service = CheckoutService(
            db,
        )

        result = service.create_checkout(

            user_id=current_user.id,

            email=request.email,

            plan_code=request.plan,

            country=request.country,

            interval=request.interval,

            success_url=request.success_url,

            cancel_url=request.cancel_url,

        )

        return CheckoutResponse(
            **result,
        )

    except ValueError as e:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(e),

        )

    except Exception as e:

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=str(e),

        )




