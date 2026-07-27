from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.billing.schemas.plan import (
    PlanResponse,
)

from app.billing.services.plan_service import (
    PlanService,
)

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.get(
    "/plans",
    response_model=list[PlanResponse],
)
def get_plans(
    db: Session = Depends(get_db),
):

    service = PlanService(
        db,
    )

    plans = service.all()

    return [

        PlanResponse.model_validate(
            plan,
        )

        for plan in plans

    ]




