from dataclasses import dataclass

from app.services.knowledge.resume_knowledge import (
    ResumeKnowledge,
)

from .jd_knowledge import JDKnowledge


@dataclass
class SkillComparison:

    matched: set[str]

    missing: set[str]

    extra: set[str]


class SkillComparator:

    @staticmethod
    def compare(
        resume: ResumeKnowledge,
        jd: JDKnowledge,
    ) -> SkillComparison:

        resume_skills = set()

        resume_skills.update(resume.frontend)
        resume_skills.update(resume.backend)
        resume_skills.update(resume.database)
        resume_skills.update(resume.programming_languages)
        resume_skills.update(resume.cloud)
        resume_skills.update(resume.devops)
        resume_skills.update(resume.tools)

        # Normalize resume skills
        resume_lookup = {
            skill.lower(): skill
            for skill in resume_skills
        }

        # Normalize JD skills
        jd_lookup = {
            skill.lower(): skill
            for skill in jd.required
        }

        matched_keys = (
            resume_lookup.keys()
            & jd_lookup.keys()
        )

        matched = {
            resume_lookup[key]
            for key in matched_keys
        }

        missing = {
            jd_lookup[key]
            for key in (
                jd_lookup.keys()
                - resume_lookup.keys()
            )
        }

        extra = {
            resume_lookup[key]
            for key in (
                resume_lookup.keys()
                - jd_lookup.keys()
            )
        }

        return SkillComparison(
            matched=matched,
            missing=missing,
            extra=extra,
        )