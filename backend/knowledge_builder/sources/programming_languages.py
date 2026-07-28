from __future__ import annotations

from knowledge_builder.models.category import Category
from knowledge_builder.models.technology import Technology
from knowledge_builder.sources.base_source import BaseSource
from knowledge_builder.models.source_package import (
    SourcePackage,
)

class ProgrammingLanguagesSource(BaseSource):

    def load(self) -> Category:

        category = Category(

            id="programming_languages",

            name="Programming Languages",

            description="Programming languages used in software engineering.",

        )

        category.add(
            Technology(
                id="python",
                name="Python",
                category="programming_languages",
                aliases=[
                    "python3",
                    "py",
                ],
            )
        )

        category.add(
            Technology(
                id="java",
                name="Java",
                category="programming_languages",
            )
        )

        category.add(
            Technology(
                id="javascript",
                name="JavaScript",
                category="programming_languages",
                aliases=[
                    "js",
                ],
            )
        )

        category.add(
            Technology(
                id="typescript",
                name="TypeScript",
                category="programming_languages",
                aliases=[
                    "ts",
                ],
            )
        )

        return SourcePackage(
            category=category,
)