from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.plan_feature import PlanFeature
from app.database.repositories.base_repository import BaseRepository


class PlanFeatureRepository(BaseRepository[PlanFeature]):
    """
    Repository for PlanFeature database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(PlanFeature, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_plan(
        self,
        plan_id: str,
    ) -> list[PlanFeature]:
        """
        Returns all feature assignments for a plan.
        """
        return (
            self.db.query(PlanFeature)
            .filter(
                PlanFeature.plan_id == plan_id,
            )
            .all()
        )

    def get_by_feature(
        self,
        feature_id: str,
    ) -> list[PlanFeature]:
        """
        Returns all plan assignments for a feature.
        """
        return (
            self.db.query(PlanFeature)
            .filter(
                PlanFeature.feature_id == feature_id,
            )
            .all()
        )

    def get_plan_feature(
        self,
        plan_id: str,
        feature_id: str,
    ) -> PlanFeature | None:
        """
        Returns the assignment for a specific
        plan and feature.
        """
        return (
            self.db.query(PlanFeature)
            .filter(
                PlanFeature.plan_id == plan_id,
                PlanFeature.feature_id == feature_id,
            )
            .first()
        )

    def plan_has_feature(
        self,
        plan_id: str,
        feature_id: str,
    ) -> bool:
        """
        Returns True if the plan includes the feature.
        """
        return (
            self.get_plan_feature(
                plan_id,
                feature_id,
            )
            is not None
        )

    def plan_has_features(
        self,
        plan_id: str,
    ) -> bool:
        """
        Returns True if the plan has at least one feature.
        """
        return (
            self.db.query(PlanFeature)
            .filter(
                PlanFeature.plan_id == plan_id,
            )
            .first()
            is not None
        )

    def feature_assigned_to_any_plan(
        self,
        feature_id: str,
    ) -> bool:
        """
        Returns True if the feature is assigned
        to at least one plan.
        """
        return (
            self.db.query(PlanFeature)
            .filter(
                PlanFeature.feature_id == feature_id,
            )
            .first()
            is not None
        )