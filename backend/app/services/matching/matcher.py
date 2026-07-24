from app.models.resume_profile import ResumeProfile
from app.models.job_profile import JobProfile
from app.models.match_result import MatchResult


class ResumeMatcher:

    @staticmethod
    def match(
        resume: ResumeProfile,
        job: JobProfile,
    ) -> MatchResult:

        print("\n========== MATCH DEBUG ==========")

        print("Resume Skills:")
        print(resume.skills)

        print("\nJob Skills:")
        print(job.skills)

        resume_skills = {
            skill.strip().lower()
            for skill in resume.skills
        }

        job_skills = {
            skill.strip().lower()
            for skill in job.skills
        }

        print("\nNormalized Resume Skills:")
        print(resume_skills)

        print("\nNormalized Job Skills:")
        print(job_skills)

        matched_skills = sorted(
            list(resume_skills & job_skills)
        )

        missing_skills = sorted(
            list(job_skills - resume_skills)
        )

        extra_skills = sorted(
            list(resume_skills - job_skills)
        )

        print("\nMatched:")
        print(matched_skills)

        print("\nMissing:")
        print(missing_skills)

        print("\nExtra:")
        print(extra_skills)

        print("================================\n")

        if len(job_skills) == 0:
            score = 0
        else:
            score = round(
                (len(matched_skills) / len(job_skills)) * 100
            )

        return MatchResult(
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            extra_skills=extra_skills,
        )