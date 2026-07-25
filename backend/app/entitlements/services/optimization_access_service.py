from sqlalchemy.orm import Session

from app.entitlements.services.entitlement_service import (
    EntitlementService,
)

from app.entitlements.services.usage_service import (
    UsageService,
)


class OptimizationAccessService:

    FEATURE = "monthly_resume_optimizations"

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.entitlements = EntitlementService(
            db
        )

        self.usage = UsageService(
            db
        )

    def check(
        self,
        user_id: str,
    ) -> tuple[bool, str]:

        limit = self.entitlements.integer_limit(

            user_id,

            self.FEATURE,

        )

        # Unlimited plan
        if limit is None:

            return (
                True,
                "Unlimited plan",
            )

        used = self.usage.month_usage(

            user_id,

            self.FEATURE,

        )

        if used >= limit:

            return (
                False,
                f"Monthly limit reached ({limit}).",
            )

        return (
            True,
            f"{limit - used} optimizations remaining.",
        )

    def consume(
        self,
        user_id: str,
    ):

        self.usage.add(

            user_id=user_id,

            feature_code=self.FEATURE,

        )