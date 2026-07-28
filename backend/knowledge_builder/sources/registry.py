from __future__ import annotations

from knowledge_builder.sources.base_source import BaseSource
from knowledge_builder.sources.programming_languages import (
    ProgrammingLanguagesSource,
)
from knowledge_builder.sources.frameworks import (
    FrameworksSource,
)


class SourceRegistry:
    """
    Registers every available knowledge source.
    """

    @staticmethod
    def all() -> list[BaseSource]:

        return [

            ProgrammingLanguagesSource(),

            FrameworksSource(),

        ]