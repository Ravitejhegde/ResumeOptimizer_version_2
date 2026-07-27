from __future__ import annotations

from app.engine.models.role_profile import (
    RoleProfile,
)


class RoleDetector:
    """
    Detects the primary job role from
    the extracted Job Description skills.

    This module performs NO AI calls.

    It uses rule-based detection built
    on the Knowledge Base.
    """

    ROLE_RULES = {

        "Full Stack Developer": {
            "python",
            "fastapi",
            "react",
            "typescript",
            "javascript",
            "docker",
        },

        "Backend Developer": {
            "python",
            "fastapi",
            "django",
            "flask",
            "postgresql",
            "redis",
        },

        "Frontend Developer": {
            "react",
            "angular",
            "vue",
            "typescript",
            "javascript",
            "html",
            "css",
        },

        "AI / ML Engineer": {
            "tensorflow",
            "pytorch",
            "opencv",
            "yolo",
            "machine learning",
            "deep learning",
            "llm",
            "langchain",
            "openai api",
        },

        "DevOps Engineer": {
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "terraform",
            "jenkins",
        },
    }

    ROLE_CATEGORIES = {

        "Full Stack Developer": [
            "Frontend",
            "Backend",
            "Database",
            "Cloud",
        ],

        "Backend Developer": [
            "Backend",
            "Database",
            "Cloud",
        ],

        "Frontend Developer": [
            "Frontend",
        ],

        "AI / ML Engineer": [
            "Artificial Intelligence",
            "Backend",
            "Cloud",
        ],

        "DevOps Engineer": [
            "DevOps",
            "Cloud",
        ],
    }

    @classmethod
    def detect(
        cls,
        skills: list[str],
    ) -> RoleProfile:

        normalized = {
            skill.lower()
            for skill in skills
        }

        best_role = "General Software Engineer"

        best_score = 0

        for role, role_skills in cls.ROLE_RULES.items():

            score = len(
                normalized.intersection(
                    role_skills
                )
            )

            if score > best_score:

                best_score = score

                best_role = role

        confidence = min(
            1.0,
            best_score / 6,
        )

        return RoleProfile(

            role=best_role,

            confidence=confidence,

            categories=cls.ROLE_CATEGORIES.get(
                best_role,
                [],
            ),

            primary_skills=[],

            secondary_skills=[],
        )




