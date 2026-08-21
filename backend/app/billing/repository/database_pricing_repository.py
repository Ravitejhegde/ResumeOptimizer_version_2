from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.plan import Plan
from app.database.models.pricing import Pricing


class DatabasePricingRepository:
    """
    Billing pricing database repository.

    Responsibilities:
        - Retrieve pricing by plan and country.
        - Retrieve active pricing for a country.
        - Keep database access separate from billing business logic.

    Does not:
        - Handle payment-provider logic.
        - Create checkout sessions.
        - Apply billing business rules.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Queries
    # ==========================================================

    def get(
        self,
        plan_code: str,
        country: str,
    ) -> Pricing | None:
        """
        Return active pricing for a plan and country.
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

        Only pricing belonging to active plans is returned.
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