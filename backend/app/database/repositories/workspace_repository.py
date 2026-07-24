from sqlalchemy.orm import Session

from app.database.models.workspace import Workspace
from app.database.repositories.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository[Workspace]):
    """
    Repository for Workspace operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Workspace,
            db,
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> Workspace | None:

        return (
            self.db.query(Workspace)
            .filter(
                Workspace.user_id == user_id,
            )
            .first()
        )