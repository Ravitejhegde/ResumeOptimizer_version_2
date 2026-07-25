from sqlalchemy.orm import Session

from app.billing.repository.database_plan_repository import (
    DatabasePlanRepository,
)


class PlanService:
    """
    Billing plan business logic.
    """

    def __init__(
        self,
        db: Session,
    ):

        self.repository = DatabasePlanRepository(
            db,
        )

    def all(self):

        return self.repository.all()

    def get(
        self,
        code: str,
    ):

        return self.repository.get_by_code(
            code,
        )