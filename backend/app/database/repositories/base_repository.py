from __future__ import annotations

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

from app.database.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(
    Generic[ModelType],
):
    """
    Base repository providing common CRUD operations.
    """

    def __init__(
        self,
        model: type[ModelType],
        db: Session,
    ) -> None:

        self.model = model
        self.db = db

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get(
        self,
        object_id: str,
    ) -> ModelType | None:

        return (
            self.db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
        )

    def get_all(
        self,
    ) -> list[ModelType]:

        return (
            self.db.query(self.model)
            .all()
        )

    def exists(
        self,
        object_id: str,
    ) -> bool:

        return self.get(object_id) is not None

    def count(
        self,
    ) -> int:

        return (
            self.db.query(self.model)
            .count()
        )

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.commit()
        self.db.refresh(instance)

        return instance

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(
        self,
        instance: ModelType,
    ) -> None:

        self.db.delete(instance)
        self.db.commit()

    def delete_by_id(
        self,
        object_id: str,
    ) -> bool:

        instance = self.get(
            object_id
        )

        if instance is None:
            return False

        self.delete(
            instance
        )

        return True




