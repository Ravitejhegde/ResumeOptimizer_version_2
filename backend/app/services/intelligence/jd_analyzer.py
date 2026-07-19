import re

from app.services.intelligence.constants import (
    TECHNOLOGY_CATEGORY,
)

from app.services.intelligence.models import (
    JDAnalysis,
    Skill,
)

from app.services.intelligence.detectors.technology_normalizer import (
    TechnologyNormalizer,
)


class JDAnalyzer:

    @staticmethod
    def analyze(
        job_description: str,
    ) -> JDAnalysis:

        text = TechnologyNormalizer.normalize(
    job_description
)

        required_skills: list[Skill] = []

        preferred_skills: list[Skill] = []

        responsibilities: list[str] = []

        # ------------------------------------
        # Technology Detection
        # ------------------------------------

        for technology, category in TECHNOLOGY_CATEGORY.items():

            if technology in text:

                required_skills.append(

                    Skill(

                        name=technology,

                        category=category,

                        section="",

                        source="jd",

                    )

                )

        # ------------------------------------
        # Responsibilities
        # ------------------------------------

        for line in job_description.splitlines():

            line = line.strip()

            if len(line) < 8:

                continue

            responsibilities.append(
                line
            )

        # ------------------------------------
        # Target Role Detection
        # ------------------------------------

        target_role = "Software Engineer"

        frontend = {

            "react",

            "angular",

            "vue",

            "next.js",

        }

        backend = {

            "node.js",

            "spring boot",

            "fastapi",

        }

        ai = {

            "tensorflow",

            "opencv",

            "yolo",

        }

        found = {

            skill.name

            for skill in required_skills

        }

        if len(frontend & found) >= 2 and len(
            backend & found
        ) >= 1:

            target_role = "Full Stack Developer"

        elif len(frontend & found) >= 2:

            target_role = "Frontend Developer"

        elif len(backend & found) >= 2:

            target_role = "Backend Developer"

        elif len(ai & found) >= 2:

            target_role = "AI/ML Engineer"

        return JDAnalysis(

            target_role=target_role,

            required_skills=required_skills,

            preferred_skills=preferred_skills,

            responsibilities=responsibilities,

        )