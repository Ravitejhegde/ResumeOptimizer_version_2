from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.models.plan_feature import PlanFeature
from app.database.models.subscription import Subscription
from app.database.models.order import Order
from app.database.models.pricing import Pricing
from app.database.models.plan import Plan


class EntitlementService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def feature_value(
        self,
        user_id: str,
        feature_code: str,
    ) -> str | None:

        subscription = (

            self.db.query(
                Subscription
            )

            .filter(

                Subscription.user_id
                == user_id,

                Subscription.status
                == "active",

            )

            .first()

        )

        if subscription is None:
            return None

        order = subscription.order

        pricing = order.pricing

        plan = pricing.plan

        feature = (

            self.db.query(
                Feature
            )

            .filter(

                Feature.code
                == feature_code,

                Feature.active == True,

            )

            .first()

        )

        if feature is None:
            return None

        plan_feature = (

            self.db.query(
                PlanFeature
            )

            .filter(

                PlanFeature.plan_id
                == plan.id,

                PlanFeature.feature_id
                == feature.id,

                PlanFeature.active == True,

            )

            .first()

        )

        if plan_feature is None:
            return None

        return plan_feature.value

    def has_feature(
        self,
        user_id: str,
        feature_code: str,
    ) -> bool:

        value = self.feature_value(

            user_id,

            feature_code,

        )

        if value is None:
            return False

        return value.lower() == "true"

    def integer_limit(
        self,
        user_id: str,
        feature_code: str,
    ) -> int | None:

        value = self.feature_value(

            user_id,

            feature_code,

        )

        if value is None:
            return None

        if value.lower() == "unlimited":
            return None

        return int(value)