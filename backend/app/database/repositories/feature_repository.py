from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.repositories.base_repository import BaseRepository


class FeatureRepository(BaseRepository[Feature]):
    """
    Repository for Feature database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Feature, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_code(
        self,
        code: str,
    ) -> Feature | None:
        """
        Returns a feature by its unique code.
        """
        return (
            self.db.query(Feature)
            .filter(
                Feature.code == code,
            )
            .first()
        )

    def get_active(
        self,
    ) -> list[Feature]:
        """
        Returns all active features ordered by name.
        """
        return (
            self.db.query(Feature)
            .filter(
                Feature.active.is_(True),
            )
            .order_by(
                Feature.name,
            )
            .all()
        )

    def code_exists(
        self,
        code: str,
    ) -> bool:
        """
        Returns True if the feature code already exists.
        """
        return self.get_by_code(code) is not None

    def active_feature_exists(
        self,
    ) -> bool:
        """
        Returns True if at least one active feature exists.
        """
        return (
            self.db.query(Feature)
            .filter(
                Feature.active.is_(True),
            )
            .first()
            is not None
        )

    # ==========================================================
    # State Management
    # ==========================================================

    def activate(
        self,
        feature: Feature,
    ) -> Feature:
        """
        Activates a feature.
        """
        feature.active = True
        return self.update(feature)

    def deactivate(
        self,
        feature: Feature,
    ) -> Feature:
        """
        Deactivates a feature.
        """
        feature.active = False
        return self.update(feature)