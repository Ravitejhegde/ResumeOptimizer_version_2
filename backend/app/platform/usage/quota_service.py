from app.platform.config.plans import PLANS
from app.platform.config.settings import SETTINGS

from .usage_service import UsageService


class QuotaService:

    @classmethod
    def can_optimize(
        cls,
        identity_id: str,
        plan: str = SETTINGS.DEFAULT_PLAN,
    ) -> bool:

        usage = UsageService.get_or_create(identity_id)

        plan_config = PLANS[plan]

        if plan_config.optimization_limit == -1:
            return True

        return (
            usage.optimizations
            < plan_config.optimization_limit
        )

    @classmethod
    def remaining_optimizations(
        cls,
        identity_id: str,
        plan: str = SETTINGS.DEFAULT_PLAN,
    ) -> int:

        usage = UsageService.get_or_create(identity_id)

        plan_config = PLANS[plan]

        if plan_config.optimization_limit == -1:
            return -1

        return max(
            0,
            plan_config.optimization_limit
            - usage.optimizations,
        )