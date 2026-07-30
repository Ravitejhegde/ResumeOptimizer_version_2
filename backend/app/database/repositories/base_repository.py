from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.

    All entity-specific repositories should inherit from this class.
    """

    def __init__(
        self,
        model: type[ModelType],
        db: Session,
    ) -> None:
        self.model = model
        self.db = db

    # ==========================================================
    # Read
    # ==========================================================

    def get(
        self,
        object_id: str,
    ) -> ModelType | None:
        """
        Returns an object by its primary key.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
        )

    def get_all(
        self,
    ) -> list[ModelType]:
        """
        Returns all records.
        """
        return (
            self.db.query(self.model)
            .all()
        )

    def exists(
        self,
        object_id: str,
    ) -> bool:
        """
        Returns True if the object exists.
        """
        return self.get(object_id) is not None

    def count(
        self,
    ) -> int:
        """
        Returns the total number of records.
        """
        return (
            self.db.query(self.model)
            .count()
        )

    # ==========================================================
    # Create
    # ==========================================================

    def create(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Persists a new object.
        """
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def create_many(
        self,
        instances: list[ModelType],
    ) -> list[ModelType]:
        """
        Persists multiple objects.
        """
        self.db.add_all(instances)
        self.db.commit()

        for instance in instances:
            self.db.refresh(instance)

        return instances

    # ==========================================================
    # Update
    # ==========================================================

    def update(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Commits changes made to an existing object.
        """
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def refresh(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Refreshes an object from the database.
        """
        self.db.refresh(instance)
        return instance

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(
        self,
        instance: ModelType,
    ) -> None:
        """
        Deletes an object.
        """
        self.db.delete(instance)
        self.db.commit()

    def delete_by_id(
        self,
        object_id: str,
    ) -> bool:
        """
        Deletes an object by its primary key.
        """
        instance = self.get(object_id)

        if instance is None:
            return False

        self.delete(instance)
        return True

    def delete_all(
        self,
    ) -> int:
        """
        Deletes all records.

        Returns:
            Number of deleted rows.
        """
        deleted = (
            self.db.query(self.model)
            .delete()
        )

        self.db.commit()

        return deleted