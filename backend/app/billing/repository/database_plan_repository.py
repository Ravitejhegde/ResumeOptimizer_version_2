from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.plan import Plan


class DatabasePlanRepository:
    """
    Billing plan database repository.

    Responsibilities:
        - Retrieve plans by code.
        - Retrieve available plans.

    Does not:
        - Handle payment-provider logic.
        - Handle checkout.
        - Apply billing business rules.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Queries
    # ==========================================================

    def get(
        self,
        plan_code: str,
    ) -> Plan | None:
        """
        Return a plan by its code.
        """
        return (
            self.db.query(Plan)
            .filter(
                Plan.code == plan_code,
            )
            .first()
        )

    def get_all(
        self,
    ) -> list[Plan]:
        """
        Return all available plans.
        """
        return (
            self.db.query(Plan)
            .all()
        )