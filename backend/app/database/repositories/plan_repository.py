from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.plan import Plan
from app.database.repositories.base_repository import BaseRepository


class PlanRepository(BaseRepository[Plan]):
    """
    Repository for Plan database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Plan, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_code(
        self,
        code: str,
    ) -> Plan | None:
        """
        Returns a plan by its unique code.
        """
        return (
            self.db.query(Plan)
            .filter(
                Plan.code == code,
            )
            .first()
        )

    def get_active(
        self,
    ) -> list[Plan]:
        """
        Returns all active plans ordered by name.
        """
        return (
            self.db.query(Plan)
            .filter(
                Plan.active.is_(True),
            )
            .order_by(
                Plan.name,
            )
            .all()
        )

    def code_exists(
        self,
        code: str,
    ) -> bool:
        """
        Returns True if the plan code already exists.
        """
        return self.get_by_code(code) is not None

    def active_plan_exists(
        self,
    ) -> bool:
        """
        Returns True if at least one active plan exists.
        """
        return (
            self.db.query(Plan)
            .filter(
                Plan.active.is_(True),
            )
            .first()
            is not None
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        plan: Plan,
    ) -> Plan:
        """
        Activates a plan.
        """
        plan.active = True
        return self.update(plan)

    def deactivate(
        self,
        plan: Plan,
    ) -> Plan:
        """
        Deactivates a plan.
        """
        plan.active = False
        return self.update(plan)