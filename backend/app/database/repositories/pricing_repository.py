from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.pricing import Pricing
from app.database.repositories.base_repository import BaseRepository


class PricingRepository(BaseRepository[Pricing]):
    """
    Repository for Pricing database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Pricing, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_plan(
        self,
        plan_id: str,
    ) -> list[Pricing]:
        """
        Returns all pricing records for a plan.
        """
        return (
            self.db.query(Pricing)
            .filter(
                Pricing.plan_id == plan_id,
            )
            .all()
        )

    def get_active(
        self,
    ) -> list[Pricing]:
        """
        Returns all active pricing records.
        """
        return (
            self.db.query(Pricing)
            .filter(
                Pricing.active.is_(True),
            )
            .all()
        )

    def get_by_country(
        self,
        country_code: str,
    ) -> list[Pricing]:
        """
        Returns all active pricing records
        for the specified country.
        """
        return (
            self.db.query(Pricing)
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
        """
        Returns the active pricing for a plan
        in the specified country.
        """
        return (
            self.db.query(Pricing)
            .filter(
                Pricing.plan_id == plan_id,
                Pricing.country_code == country_code,
                Pricing.active.is_(True),
            )
            .first()
        )

    def plan_has_pricing(
        self,
        plan_id: str,
    ) -> bool:
        """
        Returns True if the plan has at least
        one pricing configuration.
        """
        return (
            self.db.query(Pricing)
            .filter(
                Pricing.plan_id == plan_id,
            )
            .first()
            is not None
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        pricing: Pricing,
    ) -> Pricing:
        """
        Activates a pricing record.
        """
        pricing.active = True
        return self.update(pricing)

    def deactivate(
        self,
        pricing: Pricing,
    ) -> Pricing:
        """
        Deactivates a pricing record.
        """
        pricing.active = False
        return self.update(pricing)