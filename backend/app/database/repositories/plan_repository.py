from sqlalchemy.orm import Session

from app.database.models.plan import Plan
from app.database.repositories.base_repository import (
    BaseRepository,
)


class PlanRepository(
    BaseRepository[Plan],
):
    """
    Repository for Plan operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Plan,
            db,
        )

    def get_by_code(
        self,
        code: str,
    ) -> Plan | None:

        return (
            self.db.query(
                Plan
            )
            .filter(
                Plan.code == code
            )
            .first()
        )

    def get_active(
        self,
    ) -> list[Plan]:

        return (
            self.db.query(
                Plan
            )
            .filter(
                Plan.active.is_(True)
            )
            .order_by(
                Plan.name
            )
            .all()
        )

    def exists(
        self,
        code: str,
    ) -> bool:

        return (
            self.db.query(
                Plan
            )
            .filter(
                Plan.code == code
            )
            .first()
            is not None
        )
    