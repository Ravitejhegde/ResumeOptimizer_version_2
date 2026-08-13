"""
app.knowledge.provider
~~~~~~~~~~~~~~~~~~~~~~

Single access point to the application's knowledge runtime.

Every component (Analyzer, Planner, Optimizer, AI, etc.)
should obtain knowledge through this provider.

The Knowledge Builder is NEVER imported by the application.
"""

from __future__ import annotations

from functools import lru_cache

from app.knowledge.runtime import (
    KnowledgeRuntime,
    load_runtime,
)


@lru_cache(maxsize=1)
def get_knowledge() -> KnowledgeRuntime:
    """
    Return the singleton KnowledgeRuntime.

    The runtime is loaded only once and then reused for the
    lifetime of the application.
    """
    return load_runtime()