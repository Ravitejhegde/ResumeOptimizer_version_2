from __future__ import annotations

from sqlalchemy.orm import Session

from app.billing.repository.database_pricing_repository import (
    DatabasePricingRepository,
)
from app.database.models.feature import Feature
from app.database.models.plan_feature import PlanFeature


class PricingService:
    """
    Billing pricing business logic.

    Responsible for converting database pricing records
    into data required by the API.
    """

    RESUME_OPTIMIZATION_FEATURE = "resume_optimization"

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self.repository = DatabasePricingRepository(
            db,
        )

    def by_country(
        self,
        country: str,
    ):
        """
        Return active commercial pricing for a country.
        """

        pricing_items = self.repository.by_country(
            country,
        )

        return [
            self._build_response(item)
            for item in pricing_items
        ]

    def get(
        self,
        plan_code: str,
        country: str,
    ):
        """
        Return pricing for one plan and country.
        """

        pricing = self.repository.get(
            plan_code,
            country,
        )

        if pricing is None:
            return None

        return self._build_response(
            pricing,
        )

    def _build_response(
        self,
        pricing,
    ) -> dict:
        """
        Convert a Pricing model into an API-friendly
        pricing representation.
        """

        plan = pricing.plan

        plan_feature = (
            self.db.query(PlanFeature)
            .join(
                Feature,
                PlanFeature.feature_id == Feature.id,
            )
            .filter(
                PlanFeature.plan_id == plan.id,
                PlanFeature.active.is_(True),
                Feature.code
                == self.RESUME_OPTIMIZATION_FEATURE,
                Feature.active.is_(True),
            )
            .first()
        )

        if plan_feature is None:
            raise ValueError(
                f"Resume optimization limit is not configured "
                f"for plan '{plan.code}'."
            )

        try:
            monthly_optimizations = int(
                plan_feature.value,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid resume optimization limit "
                f"for plan '{plan.code}': "
                f"{plan_feature.value}"
            ) from exc

        return {
            "id": pricing.id,
            "plan_code": plan.code,
            "plan_name": plan.name,
            "plan_description": plan.description,
            "country_code": pricing.country_code,
            "currency_code": pricing.currency_code,
            "monthly_price": float(
                pricing.monthly_price,
            ),
            "yearly_price": (
                float(pricing.yearly_price)
                if pricing.yearly_price is not None
                else None
            ),
            "monthly_optimizations": monthly_optimizations,
            "payment_provider": pricing.payment_provider,
            "active": pricing.active,
        }