from __future__ import annotations

import logging

from app.engine.ai.models.resume_context import (
    ResumeContext,
)

from app.engine.models.document.document import (
    Document,
)


logger = logging.getLogger(__name__)


class ResumeContextBuilder:
    """
    Converts internal Document model into
    AI-friendly ResumeContext.

    Flow:

        Document Model
              |
              v
        ResumeContext
              |
              v
        PromptBuilder
              |
              v
        AI


    Responsibilities:

        - Extract candidate information.
        - Extract resume sections.
        - Preserve document structure information.
        - Prepare AI input.


    Does NOT:

        - Rewrite resume.
        - Call AI.
        - Modify document.
    """


    def build(
        self,
        document: Document,
    ) -> ResumeContext:
        """
        Build AI resume context.
        """


        context = ResumeContext()


        paragraphs = (
            document.paragraphs
        )


        context.paragraph_count = (
            len(paragraphs)
        )


        sections: list[str] = []

        bullet_count = 0



        for paragraph in paragraphs:


            if paragraph.section:

                section = str(
                    paragraph.section
                ).lower()


                if section not in sections:

                    sections.append(
                        section
                    )


            text = (
                paragraph.text.strip()
            )


            if not text:

                continue



            # ----------------------------------
            # Section extraction
            # ----------------------------------

            section = (
                str(
                    paragraph.section
                ).lower()
                if paragraph.section
                else ""
            )



            if section == "summary":

                if context.summary:

                    context.summary += (
                        " "
                        +
                        text
                    )

                else:

                    context.summary = text



            elif section == "experience":

                context.experience.append(

                    {
                        "text": text,
                        "id": paragraph.id,
                    }

                )



            elif section == "projects":

                context.projects.append(

                    {
                        "text": text,
                        "id": paragraph.id,
                    }

                )



            elif section == "skills":

                context.skills.setdefault(
                    "general",
                    [],
                ).append(
                    text
                )



            elif section == "education":

                context.education.append(

                    {
                        "text": text,
                        "id": paragraph.id,
                    }

                )



            # ----------------------------------
            # Bullet estimation
            # ----------------------------------

            if text.startswith(
                ("•", "-", "*")
            ):

                bullet_count += 1



        context.original_sections = (
            sections
        )


        context.bullet_count = (
            bullet_count
        )


        logger.info(

            "[ResumeContextBuilder] "
            "sections=%s paragraphs=%s",

            len(sections),

            len(paragraphs),

        )


        return context