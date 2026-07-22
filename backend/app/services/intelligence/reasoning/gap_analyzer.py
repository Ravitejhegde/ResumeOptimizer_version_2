from .models import SkillGap

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)


class GapAnalyzer:
    """
    Compares ResumeKnowledge technologies with
    Job Description technologies.
    """

    @classmethod
    def analyze(
        cls,
        resume_skills: set[str],
        jd_skills: set[str],
    ):

        matched = []
        missing = []
        extra = []

        # -----------------------------------
        # Matched & Missing
        # -----------------------------------

        for jd_skill in sorted(jd_skills):

            found = False

            for resume_skill in resume_skills:

                if TechnologyMatcher.equals(
                    resume_skill,
                    jd_skill,
                ):

                    matched.append(
                        resume_skill
                    )

                    found = True

                    break

            if not found:

                missing.append(

                    SkillGap(

                        name=jd_skill,

                        category="Technology",

                        priority=50,

                        confidence=100,

                        required=True,

                        reason="Required by Job Description",

                        matched_by="No Match",

                        related_skills=[],

                        recommendation=(
                            "Add this skill only if you have real experience."
                        ),

                    )

                )

        # -----------------------------------
        # Extra Skills
        # -----------------------------------

        for resume_skill in sorted(resume_skills):

            found = False

            for jd_skill in jd_skills:

                if TechnologyMatcher.equals(
                    resume_skill,
                    jd_skill,
                ):

                    found = True

                    break

            if not found:

                extra.append(
                    resume_skill
                )

        return (
            matched,
            missing,
            extra,
        )