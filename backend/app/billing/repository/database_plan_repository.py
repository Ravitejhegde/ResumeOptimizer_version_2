from sqlalchemy.orm import Session

from app.database.models.plan import Plan


class DatabasePlanRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def all(
        self,
    ) -> list[Plan]:

        return (

            self.db.query(Plan)

            .filter(
                Plan.active == True
            )

            .order_by(
                Plan.name
            )

            .all()

        )

    def get_by_code(
        self,
        code: str,
    ) -> Plan | None:

        return (

            self.db.query(Plan)

            .filter(

                Plan.code == code,

                Plan.active == True,

            )

            .first()

        )




