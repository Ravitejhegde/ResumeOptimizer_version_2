from sqlalchemy.orm import Session

from app.database.models.pricing import Pricing
from app.database.repositories.base_repository import (
    BaseRepository,
)


class PricingRepository(
    BaseRepository[Pricing],
):
    """
    Repository for Pricing operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Pricing,
            db,
        )

    def get_by_plan(
        self,
        plan_id: str,
    ) -> list[Pricing]:

        return (
            self.db.query(
                Pricing
            )
            .filter(
                Pricing.plan_id == plan_id
            )
            .all()
        )

    def get_by_country(
        self,
        country_code: str,
    ) -> list[Pricing]:

        return (
            self.db.query(
                Pricing
            )
            .filter(
                Pricing.country_code == country_code,
                Pricing.active.is_(True),
            )
            .all()
        )

    def get_plan_price(
        self,
        plan_id: str,
        country_code: str,
    ) -> Pricing | None:

        return (
            self.db.query(
                Pricing
            )
            .filter(
                Pricing.plan_id == plan_id,
                Pricing.country_code == country_code,
                Pricing.active.is_(True),
            )
            .first()
        )




