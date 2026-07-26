from __future__ import annotations

from copy import deepcopy

from app.engine.models.document import Document


class RollbackManager:
    """
    Restores a previously backed-up document.

    Used when validation or writing fails.
    """

    @staticmethod
    def restore(
        backup: Document,
    ) -> Document:

        return deepcopy(backup)