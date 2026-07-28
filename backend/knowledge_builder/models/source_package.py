from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.models.category import Category
from knowledge_builder.models.relationship import Relationship
from knowledge_builder.models.synonym import Synonym


@dataclass(slots=True)
class SourcePackage:

    category: Category

    relationships: list[Relationship] = field(
        default_factory=list,
    )

    synonyms: list[Synonym] = field(
        default_factory=list,
    )