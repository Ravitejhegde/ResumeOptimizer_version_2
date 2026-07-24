from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.repositories.base_repository import (
    BaseRepository,
)


class FeatureRepository(
    BaseRepository[Feature],
):
    """
    Repository for Feature operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Feature,
            db,
        )

    def get_by_code(
        self,
        code: str,
    ) -> Feature | None:

        return (
            self.db.query(
                Feature
            )
            .filter(
                Feature.code == code
            )
            .first()
        )

    def get_active(
        self,
    ) -> list[Feature]:

        return (
            self.db.query(
                Feature
            )
            .filter(
                Feature.active.is_(True)
            )
            .order_by(
                Feature.name
            )
            .all()
        )

    def exists(
        self,
        code: str,
    ) -> bool:

        return (
            self.db.query(
                Feature
            )
            .filter(
                Feature.code == code
            )
            .first()
            is not None
        )