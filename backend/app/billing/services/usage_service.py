from app.billing.services.pricing_service import (
    PricingService,
)


class UsageService:
    """
    Handles feature usage and limits.

    This service never hardcodes limits.
    Limits are always loaded from pricing.json.
    """

    def __init__(self):

        self.pricing = PricingService()

    def limits(
        self,
        *,
        country: str,
        plan: str,
    ) -> dict:

        return self.pricing.limits(

            country=country,

            plan=plan,

        )

    def limit(
        self,
        *,
        country: str,
        plan: str,
        feature: str,
    ) -> int:

        limits = self.limits(

            country=country,

            plan=plan,

        )

        return limits.get(

            feature,

            0,

        )

    def unlimited(
        self,
        *,
        country: str,
        plan: str,
        feature: str,
    ) -> bool:

        return self.limit(

            country=country,

            plan=plan,

            feature=feature,

        ) == -1

    def can_use(
        self,
        *,
        country: str,
        plan: str,
        feature: str,
        current_usage: int,
    ) -> bool:

        limit = self.limit(

            country=country,

            plan=plan,

            feature=feature,

        )

        if limit == -1:

            return True

        return current_usage < limit

    def remaining(
        self,
        *,
        country: str,
        plan: str,
        feature: str,
        current_usage: int,
    ) -> int:

        limit = self.limit(

            country=country,

            plan=plan,

            feature=feature,

        )

        if limit == -1:

            return -1

        remaining = limit - current_usage

        return max(

            remaining,

            0,

        )

    def usage_summary(
        self,
        *,
        country: str,
        plan: str,
        current_usage: dict,
    ) -> dict:

        limits = self.limits(

            country=country,

            plan=plan,

        )

        summary = {}

        for feature, limit in limits.items():

            used = current_usage.get(

                feature,

                0,

            )

            summary[feature] = {

                "used": used,

                "limit": limit,

                "remaining": -1
                if limit == -1
                else max(limit - used, 0),

                "unlimited": limit == -1,

                "allowed": True
                if limit == -1
                else used < limit,

            }

        return summary