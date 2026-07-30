from __future__ import annotations

import logging

from app.engine.ai.models.resume_context import (
    ResumeContext,
)

from app.engine.ai.models.job_context import (
    JobContext,
)


logger = logging.getLogger(__name__)


class HallucinationGuard:
    """
    Protects AI optimization from unsupported changes.

    Purpose:

        Prevent AI from creating:

            ❌ Fake experience
            ❌ Fake companies
            ❌ Fake projects
            ❌ Unsupported technologies
            ❌ Changed identity


    Flow:

        ResumeContext
              +
        JobContext
              |
              v

        HallucinationGuard

              |
              v

        PromptBuilder instructions


    Does NOT:

        - Call AI.
        - Rewrite content.
        - Validate final response.

    Final AI response validation will be
    implemented separately.
    """



    def build_rules(
        self,
        resume: ResumeContext,
        job: JobContext,
    ) -> list[str]:
        """
        Create AI safety instructions.
        """


        rules: list[str] = []


        # --------------------------------------------------
        # Identity protection
        # --------------------------------------------------

        rules.append(
            "Never change candidate name, contact information, or personal details."
        )


        # --------------------------------------------------
        # Experience protection
        # --------------------------------------------------

        rules.append(
            "Never create fake companies, employers, internships, or employment history."
        )


        rules.append(
            "Only improve existing resume experience content."
        )


        # --------------------------------------------------
        # Technology protection
        # --------------------------------------------------

        existing_skills = (
            self._collect_resume_skills(
                resume
            )
        )


        required_skills = (
            set(
                job.all_required_skills()
            )
        )


        allowed_skills = (
            existing_skills
            |
            required_skills
        )


        if allowed_skills:

            rules.append(

                "Use only supported technologies from provided context: "
                +
                ", ".join(
                    sorted(
                        allowed_skills
                    )
                )

            )



        rules.append(
            "Do not claim hands-on experience with technologies that are not supported."
        )


        # --------------------------------------------------
        # Authenticity
        # --------------------------------------------------

        rules.append(
            "Preserve candidate authenticity. Optimize wording, do not invent achievements."
        )


        logger.info(

            "[HallucinationGuard] "
            "Generated rules=%s",

            len(rules),

        )


        return rules



    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _collect_resume_skills(
        self,
        resume: ResumeContext,
    ) -> set[str]:
        """
        Collect existing resume skills.
        """

        skills: set[str] = set()


        for category in resume.skills.values():

            for skill in category:

                skills.add(
                    skill.lower()
                )


        return skills