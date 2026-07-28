from __future__ import annotations

from knowledge_builder.store.knowledge_store import (
    KnowledgeStore,
)


class TaxonomyBuilder:
    """
    Builds taxonomy JSON from the KnowledgeStore.
    """

    def build(
        self,
        store: KnowledgeStore,
    ) -> dict:

        taxonomy: dict = {}

        for category in store.categories.values():

            taxonomy[category.id] = {

                "category": {

                    "id": category.id,

                    "name": category.name,

                    "description": category.description,

                },

                "technologies": [

                    {

                        "id": technology.id,

                        "name": technology.name,

                        "aliases": technology.aliases,

                        "category": technology.category,

                        "tags": technology.tags,

                        "description": technology.description,

                        "related": technology.related,

                        "official_url": technology.official_url,

                    }

                    for technology in category.technologies

                ],

            }

        return taxonomy