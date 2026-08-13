from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.plan import Plan
from app.database.models.pricing import Pricing


class DatabasePricingRepository:
    """
    Database repository for pricing configuration.

    Responsibilities:
        - Retrieve pricing by plan and country.
        - Retrieve all active pricing for a country.
        - Keep database access separate from billing business logic.
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
        Get active pricing for a specific plan and country.

        Example:
            plan_code = "bronze"
            country = "IN"
        """

        return (
            self.db.query(Pricing)
            .join(
                Plan,
                Pricing.plan_id == Plan.id,
            )
            .filter(
                Plan.code == plan_code,
                Plan.active.is_(True),
                Pricing.country_code == country.upper(),
                Pricing.active.is_(True),
            )
            .first()
        )

    def by_country(
        self,
        country: str,
    ) -> list[Pricing]:
        """
        Return all active pricing options for a country.

        The returned pricing belongs only to active plans.

        Example:
            GET /billing/pricing?country=IN

        Returns:
            Bronze
            Silver
            Gold
        """

        return (
            self.db.query(Pricing)
            .join(
                Plan,
                Pricing.plan_id == Plan.id,
            )
            .filter(
                Plan.active.is_(True),
                Pricing.country_code == country.upper(),
                Pricing.active.is_(True),
            )
            .order_by(
                Pricing.monthly_price.asc(),
            )
            .all()
        )

    def get_all(
        self,
    ) -> list[Pricing]:
        """
        Return all active pricing configurations.

        Useful for administration, testing, and future
        pricing-management functionality.
        """

        return (
            self.db.query(Pricing)
            .join(
                Plan,
                Pricing.plan_id == Plan.id,
            )
            .filter(
                Plan.active.is_(True),
                Pricing.active.is_(True),
            )
            .order_by(
                Plan.code.asc(),
                Pricing.country_code.asc(),
            )
            .all()
        )