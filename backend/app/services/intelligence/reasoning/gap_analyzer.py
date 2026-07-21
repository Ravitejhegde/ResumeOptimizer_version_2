from .models import SkillGap

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)


class GapAnalyzer:
    """
    Compares resume skills with JD skills and
    identifies matched, missing, and extra skills.
    """

    @classmethod
    def analyze(
        cls,
        resume_skills,
        jd_skills,
    ):

        matched = []
        missing = []
        extra = []

        # -----------------------------------
        # Matched & Missing
        # -----------------------------------

        for jd_skill in jd_skills:

            matched_resume_skill = None

            for resume_skill in resume_skills:

                if TechnologyMatcher.equals(
                    resume_skill.name,
                    jd_skill.name,
                ):
                    matched_resume_skill = resume_skill
                    break

            if matched_resume_skill:

                matched.append(
                    matched_resume_skill.name
                )

            else:

                missing.append(

                    SkillGap(

                        name=jd_skill.name,

                        category=getattr(
                            jd_skill,
                            "category",
                            "OTHER",
                        ),

                        priority=getattr(
                            jd_skill,
                            "priority",
                            50,
                        ),

                        confidence=100,

                        required=getattr(
                            jd_skill,
                            "required",
                            True,
                        ),

                        reason="Technology required by the Job Description but not found in the resume.",

                        matched_by="No Match",

                        related_skills=[],

                        recommendation=(
                            "Add this technology only if you have genuine experience with it."
                        ),

                    )

                )

        # -----------------------------------
        # Extra Skills
        # -----------------------------------

        for resume_skill in resume_skills:

            found = False

            for jd_skill in jd_skills:

                if TechnologyMatcher.equals(
                    resume_skill.name,
                    jd_skill.name,
                ):
                    found = True
                    break

            if not found:

                extra.append(
                    resume_skill.name
                )

        return (
            matched,
            missing,
            extra,
        )