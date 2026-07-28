from __future__ import annotations

from knowledge_builder.models.category import Category
from knowledge_builder.models.technology import Technology
from knowledge_builder.sources.base_source import BaseSource
from knowledge_builder.models.source_package import (
    SourcePackage,
)

class FrameworksSource(BaseSource):

    def load(self) -> Category:

        category = Category(

            id="frameworks",

            name="Frameworks",

            description="Software development frameworks.",

        )

        technologies = [

            Technology(
                id="react",
                name="React",
                category="frameworks",
                aliases=["reactjs"],
                tags=["frontend"],
            ),

            Technology(
                id="angular",
                name="Angular",
                category="frameworks",
                tags=["frontend"],
            ),

            Technology(
                id="vue",
                name="Vue",
                category="frameworks",
                aliases=["vuejs"],
                tags=["frontend"],
            ),

            Technology(
                id="nodejs",
                name="Node.js",
                category="frameworks",
                aliases=["node"],
                tags=["backend"],
            ),

            Technology(
                id="express",
                name="Express",
                category="frameworks",
                aliases=["expressjs"],
                tags=["backend"],
            ),

            Technology(
                id="nestjs",
                name="NestJS",
                category="frameworks",
                tags=["backend"],
            ),

            Technology(
                id="django",
                name="Django",
                category="frameworks",
                tags=["backend"],
            ),

            Technology(
                id="flask",
                name="Flask",
                category="frameworks",
                tags=["backend"],
            ),

            Technology(
                id="fastapi",
                name="FastAPI",
                category="frameworks",
                tags=["backend", "api"],
            ),

            Technology(
                id="spring",
                name="Spring",
                category="frameworks",
                tags=["backend"],
            ),

            Technology(
                id="spring_boot",
                name="Spring Boot",
                category="frameworks",
                aliases=["springboot"],
                tags=["backend"],
            ),

            Technology(
                id="hibernate",
                name="Hibernate",
                category="frameworks",
                tags=["orm"],
            ),

        ]

        for technology in technologies:
            category.add(technology)

        return SourcePackage(
            category=category,
)