from sqlalchemy.orm import Session

from app.database.models.feature import (
    Feature,
)

from app.database.models.plan import (
    Plan,
)

from app.database.models.plan_feature import (
    PlanFeature,
)


class FeatureService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def features_for_plan(
        self,
        plan_id: str,
    ) -> list[Feature]:

        return (

            self.db.query(Feature)

            .join(

                PlanFeature,

                Feature.id
                == PlanFeature.feature_id,

            )

            .join(

                Plan,

                Plan.id
                == PlanFeature.plan_id,

            )

            .filter(

                Plan.id == plan_id,

            )

            .all()

        )

    def has_feature(
        self,
        plan_id: str,
        feature_code: str,
    ) -> bool:

        return (

            self.db.query(Feature)

            .join(

                PlanFeature,

                Feature.id
                == PlanFeature.feature_id,

            )

            .filter(

                PlanFeature.plan_id
                == plan_id,

                Feature.code
                == feature_code,

            )

            .first()

            is not None

        )




