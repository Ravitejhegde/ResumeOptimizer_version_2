from sqlalchemy.orm import Session

from app.billing.repository.database_pricing_repository import (
    DatabasePricingRepository,
)


class PricingService:
    """
    Billing pricing business logic.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.repository = DatabasePricingRepository(
            db,
        )

    def by_country(
        self,
        country: str,
    ):

        return self.repository.by_country(
            country,
        )

    def get(
        self,
        plan_code: str,
        country: str,
    ):

        return self.repository.get(
            plan_code,
            country,
        )




