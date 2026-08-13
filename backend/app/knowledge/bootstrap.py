"""
app.knowledge.bootstrap
~~~~~~~~~~~~~~~~~~~~~~~

Creates the singleton Knowledge Runtime.
"""

from __future__ import annotations

from pathlib import Path

from app.knowledge.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)

_runtime: KnowledgeRuntime | None = None


def get_runtime() -> KnowledgeRuntime:
    """
    Return the application Knowledge Runtime.
    """

    global _runtime

    if _runtime is None:

        runtime = KnowledgeRuntime(
            Path("output")
        )

        runtime.load()

        _runtime = runtime

    return _runtime