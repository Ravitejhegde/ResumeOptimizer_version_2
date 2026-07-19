from app.services.intelligence.models import (
    Skill,
)


class RoleDetector:

    ROLE_RULES = {

        "AI/ML Engineer": {

            "python": 15,

            "tensorflow": 20,

            "keras": 20,

            "opencv": 20,

            "yolo": 20,

            "pytorch": 20,

            "machine learning": 25,

            "deep learning": 25,

        },

        "Frontend Developer": {

            "html": 15,

            "css": 15,

            "javascript": 20,

            "typescript": 20,

            "react": 30,

            "angular": 30,

            "vue": 30,

            "next.js": 25,

        },

        "Backend Developer": {

            "java": 20,

            "python": 15,

            "node.js": 25,

            "spring boot": 30,

            "django": 25,

            "fastapi": 25,

            "express": 25,

            "sql": 15,

            "rest api": 20,

        },

        "Full Stack Developer": {

            "react": 20,

            "angular": 20,

            "vue": 20,

            "node.js": 20,

            "spring boot": 20,

            "sql": 15,

            "git": 10,

            "rest api": 15,

            "javascript": 15,

            "typescript": 15,

        },

        "DevOps Engineer": {

            "docker": 30,

            "kubernetes": 30,

            "jenkins": 25,

            "ci/cd": 25,

            "github actions": 20,

            "aws": 20,

            "azure": 20,

        },

    }

    @staticmethod
    def detect(

        skills: list[Skill],

    ) -> str:

        scores = {

            role: 0

            for role in RoleDetector.ROLE_RULES

        }

        for skill in skills:

            name = skill.name.lower()

            for role, technologies in (

                RoleDetector.ROLE_RULES.items()

            ):

                if name in technologies:

                    scores[role] += (

                        technologies[name]

                    )

        print()

        print("========== ROLE SCORE ==========")

        for role, score in scores.items():

            print(

                f"{role:<25} {score}"

            )

        print()

        return max(

            scores,

            key=scores.get,

        )