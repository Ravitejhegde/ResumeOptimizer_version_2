from __future__ import annotations

from knowledge_builder.builders.taxonomy_builder import (
    TaxonomyBuilder,
)
from knowledge_builder.exporters.json_exporter import (
    JsonExporter,
)
from knowledge_builder.store.knowledge_store import (
    KnowledgeStore,
)


class BuildPipeline:
    """
    Executes all builders and exporters.
    """

    def run(
        self,
        store: KnowledgeStore,
    ) -> None:

        taxonomy = TaxonomyBuilder().build(
            store,
        )

        JsonExporter().export(
            taxonomy,
            "knowledge_builder/output/taxonomy",
        )