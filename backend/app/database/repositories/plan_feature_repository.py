from sqlalchemy.orm import Session

from app.database.models.plan_feature import PlanFeature
from app.database.repositories.base_repository import (
    BaseRepository,
)


class PlanFeatureRepository(
    BaseRepository[PlanFeature],
):
    """
    Repository for PlanFeature operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            PlanFeature,
            db,
        )

    def get_by_plan(
        self,
        plan_id: str,
    ) -> list[PlanFeature]:

        return (
            self.db.query(
                PlanFeature
            )
            .filter(
                PlanFeature.plan_id == plan_id
            )
            .all()
        )

    def get_by_feature(
        self,
        feature_id: str,
    ) -> list[PlanFeature]:

        return (
            self.db.query(
                PlanFeature
            )
            .filter(
                PlanFeature.feature_id == feature_id
            )
            .all()
        )

    def get_plan_feature(
        self,
        plan_id: str,
        feature_id: str,
    ) -> PlanFeature | None:

        return (
            self.db.query(
                PlanFeature
            )
            .filter(
                PlanFeature.plan_id == plan_id,
                PlanFeature.feature_id == feature_id,
            )
            .first()
        )




