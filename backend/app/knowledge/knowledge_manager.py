from __future__ import annotations

from app.knowledge.knowledge_initializer import (
    KnowledgeInitializer,
)
from app.knowledge.knowledge_registry import (
    KnowledgeRegistry,
)


class KnowledgeManager:
    """
    Public facade of the Knowledge Platform.

    Every analyzer, planner and optimizer
    accesses knowledge only through here.
    """

    def __init__(
        self,
    ) -> None:

        self._registry: KnowledgeRegistry | None = None

    # --------------------------------------------------

    def initialize(
        self,
    ) -> None:

        if self._registry is None:

            self._registry = (
                KnowledgeInitializer.initialize()
            )

    # --------------------------------------------------

    @property
    def registry(
        self,
    ) -> KnowledgeRegistry:

        self.initialize()

        return self._registry

    # --------------------------------------------------
    # Extraction
    # --------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[str]:

        return self.registry.extractor.extract(
            text,
        )

    # --------------------------------------------------
    # Normalization
    # --------------------------------------------------

    def normalize(
        self,
        value: str,
    ) -> str:

        return self.registry.normalizer.normalize(
            value,
        )

    def normalize_many(
        self,
        values: list[str],
    ) -> list[str]:

        return self.registry.normalizer.normalize_many(
            values,
        )

    # --------------------------------------------------
    # Categorization
    # --------------------------------------------------

    def categorize(
        self,
        skills: list[str],
    ):

        return self.registry.categorizer.categorize(
            skills,
        )

    def category(
        self,
        technology: str,
    ):

        return self.registry.index.category(
            technology,
        )

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    def related(
        self,
        technology: str,
    ):

        return self.registry.index.related(
            technology,
        )

    # --------------------------------------------------
    # Technologies
    # --------------------------------------------------

    def technologies(
        self,
    ):

        return (
            self.registry
            .software_engineering
            .technologies()
        )

    def technology_exists(
        self,
        technology: str,
    ):

        return (
            self.registry
            .software_engineering
            .technology_exists(
                technology,
            )
        )

    # --------------------------------------------------
    # Roles
    # --------------------------------------------------

    def role(
        self,
        role_id: str,
    ):

        return (
            self.registry
            .software_engineering
            .role(
                role_id,
            )
        )

        # --------------------------------------------------
    # Profiles
    # --------------------------------------------------

    def profile(
        self,
        profile_id: str,
    ):

        return (
            self.registry
            .software_engineering
            .profile(
                profile_id,
            )
        )

    def all_profiles(
        self,
    ):

        return (
            self.registry
            .software_engineering
            .all_profiles()
        )

    # --------------------------------------------------
    # Sections
    # --------------------------------------------------

    def section(
        self,
        section_id: str,
    ):

        return (
            self.registry
            .software_engineering
            .section(
                section_id,
            )
        )

    def all_sections(
        self,
    ):

        return (
            self.registry
            .software_engineering
            .all_sections()
        )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def metadata(
        self,
    ):

        return (
            self.registry
            .software_engineering
            .metadata_info()
        )
