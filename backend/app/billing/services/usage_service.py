from __future__ import annotations

from sqlalchemy.orm import Session

from app.billing.services.entitlement_service import (
    EntitlementService,
)


class UsageService:
    """
    Handles feature usage and entitlement limits.

    Usage limits are resolved from the user's active
    subscription through EntitlementService.

    This service does not hardcode plan limits.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.entitlements = EntitlementService(
            db,
        )

    # ==========================================================
    # Limit
    # ==========================================================

    def limit(
        self,
        *,
        user_id: str,
        feature: str,
    ) -> int | None:
        """
        Return the user's limit for a feature.

        Returns:
            Integer limit for the feature.
            None means unlimited or no configured limit.
        """

        return self.entitlements.integer_limit(
            user_id,
            feature,
        )

    # ==========================================================
    # Unlimited
    # ==========================================================

    def unlimited(
        self,
        *,
        user_id: str,
        feature: str,
    ) -> bool:
        """
        Return True when the user's feature is unlimited.
        """

        return (
            self.limit(
                user_id=user_id,
                feature=feature,
            )
            is None
        )

    # ==========================================================
    # Can Use
    # ==========================================================

    def can_use(
        self,
        *,
        user_id: str,
        feature: str,
        current_usage: int,
    ) -> bool:
        """
        Return True when the user can consume another unit
        of the requested feature.
        """

        limit = self.limit(
            user_id=user_id,
            feature=feature,
        )

        # None represents unlimited.
        if limit is None:
            return True

        return current_usage < limit

    # ==========================================================
    # Remaining
    # ==========================================================

    def remaining(
        self,
        *,
        user_id: str,
        feature: str,
        current_usage: int,
    ) -> int | None:
        """
        Return remaining feature usage.

        Returns:
            Remaining count.
            None means unlimited.
        """

        limit = self.limit(
            user_id=user_id,
            feature=feature,
        )

        if limit is None:
            return None

        return max(
            limit - current_usage,
            0,
        )

    # ==========================================================
    # Usage Summary
    # ==========================================================

    def usage_summary(
        self,
        *,
        user_id: str,
        usage: dict[str, int],
    ) -> dict:
        """
        Build a usage summary for the user's features.

        The feature list comes from the supplied usage mapping.
        """

        summary = {}

        for feature, current_usage in usage.items():

            limit = self.limit(
                user_id=user_id,
                feature=feature,
            )

            unlimited = limit is None

            summary[feature] = {
                "used": current_usage,
                "limit": limit,
                "remaining": (
                    None
                    if unlimited
                    else max(
                        limit - current_usage,
                        0,
                    )
                ),
                "unlimited": unlimited,
                "allowed": (
                    True
                    if unlimited
                    else current_usage < limit
                ),
            }

        return summary