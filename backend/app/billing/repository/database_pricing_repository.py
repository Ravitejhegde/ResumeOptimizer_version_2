from sqlalchemy.orm import Session

from app.database.models.pricing import Pricing
from app.database.models.plan import Plan


class DatabasePricingRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def by_country(
        self,
        country_code: str,
    ) -> list[Pricing]:

        return (

            self.db.query(Pricing)

            .filter(

                Pricing.country_code == country_code.upper(),

                Pricing.active == True,

            )

            .all()

        )

    def get(
        self,
        plan_code: str,
        country_code: str,
    ) -> Pricing | None:

        return (

            self.db.query(Pricing)

            .join(

                Plan,

                Pricing.plan_id == Plan.id,

            )

            .filter(

                Plan.code == plan_code,

                Plan.active == True,

                Pricing.country_code == country_code.upper(),

                Pricing.active == True,

            )

            .first()

        )

    def monthly_price(
        self,
        plan_code: str,
        country_code: str,
    ):

        pricing = self.get(

            plan_code,

            country_code,

        )

        if pricing is None:

            return None

        return pricing.monthly_price

    def yearly_price(
        self,
        plan_code: str,
        country_code: str,
    ):

        pricing = self.get(

            plan_code,

            country_code,

        )

        if pricing is None:

            return None

        return pricing.yearly_price