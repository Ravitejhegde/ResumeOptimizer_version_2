from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.workspace import Workspace
from app.database.repositories.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository[Workspace]):
    """
    Repository for Workspace database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(Workspace, db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_user_id(
        self,
        user_id: str,
    ) -> Workspace | None:
        """
        Returns the workspace owned by the given user.
        """
        return (
            self.db.query(Workspace)
            .filter(
                Workspace.user_id == user_id,
            )
            .first()
        )

    def user_has_workspace(
        self,
        user_id: str,
    ) -> bool:
        """
        Returns True if the user already has a workspace.
        """
        return self.get_by_user_id(user_id) is not None