from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.billing.schemas.pricing import PricingResponse
from app.billing.services.pricing_service import PricingService
from app.database.session import get_db


router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.get(
    "/pricing",
    response_model=list[PricingResponse],
)
def get_pricing(
    country: str = Query(
        ...,
        min_length=2,
        max_length=2,
    ),
    db: Session = Depends(get_db),
):
    """
    Return active paid pricing for a country.
    """

    service = PricingService(db)

    return service.by_country(country.upper())