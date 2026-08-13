"""
knowledge_builder.registry.loader_registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Central registry for all knowledge loaders.

Responsibilities
----------------
- Register every loader.
- Return registered loaders.
- Prevent duplicate registrations.
- Keep StoreBuilder independent from concrete loaders.
"""

from __future__ import annotations

from typing import Iterable

from knowledge_builder.contracts.loader import LoaderContract

from knowledge_builder.loaders import (
    ATSLoader,
    CategoryLoader,
    KeywordLoader,
    RelationshipLoader,
    RoleLoader,
    SectionLoader,
    SkillLoader,
    SynonymLoader,
    TechnologyLoader,
)


class LoaderRegistry:
    """
    Registry containing every knowledge loader.
    """

    def __init__(self) -> None:
        self._loaders: list[LoaderContract] = []

        self._register_defaults()

    def register(
        self,
        loader: LoaderContract,
    ) -> None:
        """
        Register a loader.

        Raises
        ------
        ValueError
            If a loader with the same name already exists.
        """

        if any(
            item.name == loader.name
            for item in self._loaders
        ):
            raise ValueError(
                f"Loader already registered: {loader.name}"
            )

        self._loaders.append(loader)

    def all(self) -> Iterable[LoaderContract]:
        """
        Return every registered loader.
        """
        return tuple(self._loaders)

    def _register_defaults(self) -> None:
        """
        Register framework loaders.
        """

        self.register(
            CategoryLoader.from_default_location()
        )

        self.register(
            TechnologyLoader.from_default_location()
        )

        self.register(
            SkillLoader.from_default_location()
        )

        self.register(
            RoleLoader.from_default_location()
        )

        self.register(
            SectionLoader.from_default_location()
        )

        self.register(
            SynonymLoader.from_default_location()
        )

        self.register(
            KeywordLoader.from_default_location()
        )

        self.register(
            RelationshipLoader.from_default_location()
        )

        self.register(
            ATSLoader.from_default_location()
        )