from typing import Generic
from typing import Type
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
        model: Type[ModelType],
        db: Session,
    ) -> None:

        self.model = model
        self.db = db

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

    def create(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def update(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.commit()
        self.db.refresh(instance)

        return instance

    def delete(
        self,
        instance: ModelType,
    ) -> None:

        self.db.delete(instance)
        self.db.commit()