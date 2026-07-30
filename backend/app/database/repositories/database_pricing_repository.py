from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.pricing import Pricing


class DatabasePricingRepository:
    """
    Billing pricing repository.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db



    def get(
        self,
        plan_code: str,
        country: str,
    ) -> Pricing | None:
        """
        Get pricing by plan and country.
        """

        return (
            self.db.query(Pricing)
            .filter(
                Pricing.plan_code == plan_code,
                Pricing.country_code == country,
            )
            .first()
        )