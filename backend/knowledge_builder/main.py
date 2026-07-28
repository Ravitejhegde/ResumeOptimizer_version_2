from __future__ import annotations

from knowledge_builder.pipeline.build_pipeline import (
    BuildPipeline,
)
from knowledge_builder.sources.source_manager import (
    SourceManager,
)
from knowledge_builder.store.knowledge_store import (
    KnowledgeStore,
)
from knowledge_builder.validators.knowledge_validator import (
    KnowledgeValidator,
)


def main() -> None:
    """
    Entry point for the Knowledge Builder.
    """

    # Load all knowledge sources
    manager = SourceManager()
    packages = manager.load_packages()

    # Build the in-memory knowledge store
    store = KnowledgeStore()
    store.load(packages)

    # Validate the knowledge
    KnowledgeValidator().validate(
        store,
    )

    # Execute the build pipeline
    BuildPipeline().run(
        store,
    )

    print(
        "Knowledge base generated successfully."
    )


if __name__ == "__main__":
    main()