from __future__ import annotations

import re

from app.engine.intelligence.technology_graph import (
    TechnologyGraph,
)


class RoleDetector:
    """
    Detects the primary job role from a
    Job Description.

    Uses:
    - Job title
    - Technology frequencies
    - Technology graph
    """

    ROLE_KEYWORDS = {

        "AI/ML Engineer": [
            "machine learning",
            "deep learning",
            "computer vision",
            "tensorflow",
            "pytorch",
            "opencv",
            "yolo",
            "llm",
            "langchain",
            "openai",
            "artificial intelligence",
            "ai engineer",
        ],

        "Full Stack Developer": [
            "full stack",
            "react",
            "typescript",
            "javascript",
            "html",
            "css",
            "python",
            "fastapi",
            "backend",
            "frontend",
        ],

        "Backend Developer": [
            "backend",
            "python",
            "fastapi",
            "django",
            "flask",
            "sqlalchemy",
            "postgresql",
            "redis",
            "rest api",
            "microservices",
        ],

        "Frontend Developer": [
            "frontend",
            "react",
            "angular",
            "vue",
            "typescript",
            "javascript",
            "html",
            "css",
        ],

        "DevOps Engineer": [
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "terraform",
            "jenkins",
            "github actions",
            "ci/cd",
            "linux",
        ],

        "Data Engineer": [
            "spark",
            "hadoop",
            "etl",
            "data warehouse",
            "airflow",
            "sql",
            "python",
        ],

    }

    def __init__(self) -> None:

        self._graph = TechnologyGraph()

    def detect(
        self,
        job_description: str,
    ) -> str:

        text = job_description.lower()

        scores: dict[str, int] = {}

        for role, keywords in self.ROLE_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                score += len(
                    re.findall(
                        re.escape(keyword),
                        text,
                    )
                )

            scores[role] = score

        if not scores:
            return "General Software Engineer"

        best_role = max(
            scores,
            key=scores.get,
        )

        if scores[best_role] == 0:
            return "General Software Engineer"

        return best_role