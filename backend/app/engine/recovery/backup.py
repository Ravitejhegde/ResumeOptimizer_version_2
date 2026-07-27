from __future__ import annotations

from copy import deepcopy

from app.engine.models.document import Document


class BackupManager:
    """
    Creates immutable backups of the document.

    A backup is created before optimization begins so
    the original document can always be restored.
    """

    @staticmethod
    def create(
        document: Document,
    ) -> Document:

        return deepcopy(document)




