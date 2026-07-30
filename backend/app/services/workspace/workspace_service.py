from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.workspace import Workspace
from app.database.repositories.workspace_repository import (
    WorkspaceRepository,
)


class WorkspaceService:
    """
    Business logic for workspace management.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.workspaces = WorkspaceRepository(db)

    # ==========================================================
    # Queries
    # ==========================================================

    def get_workspace(
        self,
        workspace_id: str,
    ) -> Workspace | None:
        """
        Returns workspace by ID.
        """
        return self.workspaces.get(workspace_id)

    def get_user_workspace(
        self,
        user_id: str,
    ) -> Workspace | None:
        """
        Returns user's workspace.
        """
        return self.workspaces.get_by_user_id(user_id)

    def user_has_workspace(
        self,
        user_id: str,
    ) -> bool:
        """
        Checks whether user already owns a workspace.
        """
        return (
            self.workspaces.get_by_user_id(user_id)
            is not None
        )

    # ==========================================================
    # Creation
    # ==========================================================

    def create_workspace(
        self,
        user_id: str,
        name: str = "My Workspace",
    ) -> Workspace:
        """
        Creates a workspace for a user.

        A user can only have one workspace.
        """

        existing = self.workspaces.get_by_user_id(
            user_id
        )

        if existing:
            return existing

        workspace = Workspace(
            user_id=user_id,
            name=name,
        )

        return self.workspaces.create(
            workspace
        )

    # ==========================================================
    # Update
    # ==========================================================

    def update_workspace(
        self,
        workspace: Workspace,
    ) -> Workspace:
        """
        Updates workspace information.
        """
        return self.workspaces.update(
            workspace
        )

    # ==========================================================
    # Delete
    # ==========================================================

    def delete_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Deletes a workspace.
        """
        self.workspaces.delete(
            workspace
        )