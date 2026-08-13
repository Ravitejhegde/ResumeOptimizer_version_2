"""
app.knowledge.runtime.knowledge_runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public entry point for the ResumeOptimizer Knowledge Runtime.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.knowledge.contracts.runtime_contract import RuntimeContract
from app.knowledge.exceptions.runtime_errors import (
    KnowledgeLoadError,
    KnowledgeNotLoadedError,
)
from app.knowledge.loaders.knowledge_loader import KnowledgeLoader
from app.knowledge.models.knowledge_model import KnowledgeModel
from app.knowledge.services.category_resolver import CategoryResolver
from app.knowledge.services.role_resolver import RoleResolver
from app.knowledge.services.skill_resolver import SkillResolver
from app.knowledge.services.technology_resolver import (
    TechnologyResolver,
)


class KnowledgeRuntime(RuntimeContract):
    """
    Public runtime entry point for the Knowledge Platform.
    """

    def __init__(
        self,
        package_directory: Path | str,
    ) -> None:

        self._loader = KnowledgeLoader(package_directory)
        self._knowledge = KnowledgeModel()

        # Runtime services
        self._categories = CategoryResolver(self._knowledge)
        self._technologies = TechnologyResolver(self._knowledge)
        self._skills = SkillResolver(self._knowledge)
        self._roles = RoleResolver(self._knowledge)

        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        """
        Return True if knowledge has been loaded.
        """
        return self._loaded

    def load(self) -> None:
        """
        Load exported knowledge.
        """
        try:
            self._knowledge.data = self._loader.load_json(
                "knowledge.json"
            )

            self._loaded = True

        except Exception as exc:
            raise KnowledgeLoadError(
                str(exc)
            ) from exc

    @property
    def knowledge(self) -> KnowledgeModel:
        """
        Return the loaded knowledge model.
        """
        if not self._loaded:
            raise KnowledgeNotLoadedError(
                "Knowledge Runtime has not been loaded."
            )

        return self._knowledge

    @property
    def categories(self) -> CategoryResolver:
        """
        Category resolver.
        """
        return self._categories

    @property
    def technologies(self) -> TechnologyResolver:
        """
        Technology resolver.
        """
        return self._technologies

    @property
    def skills(self) -> SkillResolver:
        """
        Skill resolver.
        """
        return self._skills

    @property
    def roles(self) -> RoleResolver:
        """
        Role resolver.
        """
        return self._roles


@lru_cache(maxsize=1)
def load_runtime() -> KnowledgeRuntime:
    """
    Load and cache the application Knowledge Runtime.
    """

    runtime = KnowledgeRuntime("output")
    runtime.load()
    return runtime