from sqlalchemy.orm import Session

from app.database.models.workspace import Workspace
from app.database.repositories.workspace_repository import (
    WorkspaceRepository,
)


class WorkspaceService:
    """
    Business logic for workspaces.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.workspaces = WorkspaceRepository(db)

    def get_workspace(
        self,
        workspace_id: str,
    ) -> Workspace | None:

        return self.workspaces.get(workspace_id)

    def get_by_user(
        self,
        user_id: str,
    ) -> Workspace | None:

        return self.workspaces.get_by_user_id(user_id)

    def create_workspace(
        self,
        workspace: Workspace,
    ) -> Workspace:

        return self.workspaces.create(workspace)

    def update_workspace(
        self,
        workspace: Workspace,
    ) -> Workspace:

        return self.workspaces.update(workspace)

    def delete_workspace(
        self,
        workspace: Workspace,
    ) -> None:

        self.workspaces.delete(workspace)




