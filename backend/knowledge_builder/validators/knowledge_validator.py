from __future__ import annotations

from knowledge_builder.store.knowledge_store import (
    KnowledgeStore,
)


class KnowledgeValidator:
    """
    Validates the knowledge store before export.
    """

    def validate(
        self,
        store: KnowledgeStore,
    ) -> None:

        self._validate_categories(store)

        self._validate_technologies(store)

        print("✓ Knowledge validation passed.")

    # --------------------------------------------------

    def _validate_categories(
        self,
        store: KnowledgeStore,
    ) -> None:

        for category in store.categories.values():

            if not category.id:

                raise ValueError(
                    "Category id cannot be empty."
                )

            if not category.name:

                raise ValueError(
                    f"Category '{category.id}' has no name."
                )

    # --------------------------------------------------

    def _validate_technologies(
        self,
        store: KnowledgeStore,
    ) -> None:

        seen_aliases: set[str] = set()

        for technology in store.technologies.values():

            if not technology.id:

                raise ValueError(
                    "Technology id cannot be empty."
                )

            if not technology.name:

                raise ValueError(
                    f"{technology.id} has no name."
                )

            for alias in technology.aliases:

                key = alias.lower()

                if key in seen_aliases:

                    raise ValueError(
                        f"Duplicate alias: {alias}"
                    )

                seen_aliases.add(key)