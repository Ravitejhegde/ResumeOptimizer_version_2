"""
app.knowledge.runtime
~~~~~~~~~~~~~~~~~~~~~

Runtime package for the application's knowledge layer.
"""

from .knowledge_runtime import (
    KnowledgeRuntime,
    load_runtime,
)

__all__ = [
    "KnowledgeRuntime",
    "load_runtime",
]