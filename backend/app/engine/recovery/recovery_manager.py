from __future__ import annotations

from app.engine.models.document.document import Document

from app.engine.recovery.backup import BackupManager
from app.engine.recovery.rollback import RollbackManager


class RecoveryManager:
    """
    Coordinates document recovery operations.

    Responsibilities
    ----------------
    - Create backups
    - Restore backups
    - Handle optimization failures
    - Handle writer failures
    """

    def __init__(self) -> None:

        self._backup = BackupManager()

        self._rollback = RollbackManager()

    def backup(
        self,
        document: Document,
    ) -> Document:

        return self._backup.create(document)

    def rollback(
        self,
        backup: Document,
    ) -> Document:

        return self._rollback.restore(backup)




