from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.billing.schemas.pricing import (
    PricingResponse,
)

from app.billing.services.pricing_service import (
    PricingService,
)

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.get(
    "/pricing",
    response_model=list[PricingResponse],
)
def get_pricing(
    country: str,
    db: Session = Depends(get_db),
):

    service = PricingService(
        db,
    )

    pricing = service.by_country(
        country,
    )

    return [

        PricingResponse.model_validate(
            item,
        )

        for item in pricing

    ]