from __future__ import annotations

import json
import logging
from typing import Any

from app.engine.ai.models.ai_prompt import (
    AIPrompt,
)

from app.engine.ai.context.optimization_context import (
    OptimizationContext,
)

from app.engine.ai.guardrails.format_constraints import (
    FormatConstraints,
)

from app.engine.ai.guardrails.hallucination_guard import (
    HallucinationGuard,
)

from app.engine.ai.guardrails.length_controller import (
    LengthController,
)

from app.engine.ai.guardrails.response_limits import (
    ResponseLimits,
)


logger = logging.getLogger(__name__)


class ResumePromptBuilder:
    """
    Creates the complete AI resume optimization prompt.

    Architecture:

        OptimizationContext
                |
                v

        ResumePromptBuilder

                |
                v

          Single AI Prompt

                |
                v

          OpenRouter


    Responsibilities:

        - Convert knowledge into AI instructions.
        - Provide paragraph-level resume data.
        - Preserve DOCX mapping IDs.
        - Add safety constraints.
        - Create one-call prompt.


    Does NOT:

        - Call AI.
        - Parse AI response.
        - Modify DOCX.
    """



    def __init__(
        self,
    ) -> None:


        self._format_constraints = (
            FormatConstraints()
        )


        self._length_controller = (
            LengthController()
        )


        self._response_limits = (
            ResponseLimits()
        )


        self._hallucination_guard = (
            HallucinationGuard()
        )



    # ==================================================
    # Public API
    # ==================================================

    def build(
        self,
        context: OptimizationContext,
    ) -> AIPrompt:
        """
        Build final AI prompt.
        """


        prompt = AIPrompt()


        prompt.add_message(

            role="system",

            content=self._build_system_instruction(
                context
            ),

        )


        prompt.add_message(

            role="user",

            content=self._build_user_payload(
                context
            ),

        )


        logger.info(
            "[ResumePromptBuilder] Prompt created."
        )


        return prompt



    # ==================================================
    # System Instruction
    # ==================================================

    def _build_system_instruction(
        self,
        context: OptimizationContext,
    ) -> str:
        """
        Defines AI behavior.
        """


        rules = [

            "You are an expert AI resume optimization engine.",

            "Optimize the existing resume for the given job description.",

            "Improve wording, relevance, ATS compatibility, and technical alignment.",

            "Preserve candidate authenticity.",

            "Return ONLY valid JSON.",

            "Do not return markdown.",

            "Do not provide explanations.",


            # Paragraph mapping

            "Every rewritten paragraph must keep the original paragraph_id.",

            "Never remove paragraph identifiers.",

            "Never create new paragraphs.",

            "Only optimize provided paragraphs.",


            # Formatting

            "Preserve resume structure.",

            "Do not change section order.",

            "Do not increase paragraph count.",


            # Skills

            "Do not invent skills or experience.",

            "Use job-required skills only when they can naturally fit existing content.",

        ]



        rules.extend(

            context.constraints
            .to_instruction_list()

        )


        rules.extend(

            self._format_constraints
            .to_instructions()

        )


        rules.extend(

            self._hallucination_guard
            .build_rules(

                context.resume,

                context.job,

            )

        )


        return "\n".join(
            rules
        )



    # ==================================================
    # User Payload
    # ==================================================

    def _build_user_payload(
        self,
        context: OptimizationContext,
    ) -> str:
        """
        Builds structured AI input.
        """


        payload = {

            "objective":

                context.objective,


            "resume":

                self._serialize_resume(
                    context
                ),


            "job":

                self._serialize_job(
                    context
                ),


            "knowledge":

                self._serialize_knowledge(
                    context
                ),



            "output_schema":

            {

                "candidate_name":
                    "string",


                "role_title":
                    "string",


                "summary":
                    "string",


                "paragraphs":

                    [

                        {

                            "paragraph_id":
                                "string",

                            "optimized_text":
                                "string",

                        }

                    ],


                "skills":
                    "object",

            },

        }


        return json.dumps(

            payload,

            indent=2,

            ensure_ascii=False,

        )



    # ==================================================
    # Resume Serialization
    # ==================================================

    def _serialize_resume(
        self,
        context: OptimizationContext,
    ) -> dict[str, Any]:

        resume = context.resume


        return {

            "candidate_name":

                resume.title,


            "paragraphs":

                self._serialize_paragraphs(
                    resume
                ),


            "skills":

                resume.skills,

        }



    def _serialize_paragraphs(
        self,
        resume,
    ) -> list[dict]:
        """
        Convert resume sections into AI editable paragraphs.

        Supports:
            - list based sections
            - dict based sections

        Writer requires stable paragraph_id.
        """

        paragraphs = []

        index = 0


        sections = resume.original_sections



    # ----------------------------------
    # Dictionary format
    # ----------------------------------

        if isinstance(
            sections,
            dict,
        ):

            iterator = sections.items()


    # ----------------------------------
    # List format
    # ----------------------------------

        elif isinstance(
            sections,
            list,
        ):

            iterator = []


            for section in sections:

                if isinstance(
                    section,
                    dict,
                ):

                    name = (
                        section.get(
                            "section"
                        )
                        or
                        section.get(
                            "name"
                        )
                        or
                        "unknown"
                    )


                    content = (
                        section.get(
                            "content"
                        )
                        or
                        section.get(
                            "text"
                        )
                        or
                        []
                    )


                    iterator.append(
                        (
                            name,
                            content,
                        )
                    )


        else:

            return paragraphs



        for section_name, items in iterator:


            if isinstance(
                items,
                str,
            ):

                items = [items]



            if not isinstance(
                items,
                list,
            ):

                continue



            for item in items:


                if not isinstance(
                    item,
                    str,
                ):

                    continue



                paragraphs.append(

                    {

                        "paragraph_id":
                            f"{section_name}_{index}",


                        "section":
                            section_name,


                        "original_text":
                            item,


                        "line_budget":
                            self._calculate_line_budget(
                                item
                            ),

                }

            )


            index += 1



        return paragraphs



    # ==================================================
    # Job Serialization
    # ==================================================

    def _serialize_job(
        self,
        context: OptimizationContext,
    ) -> dict[str, Any]:

        job = context.job


        return {

            "role":

                job.role_title,


            "required_skills":

                job.required_skills,


            "preferred_skills":

                job.preferred_skills,


            "responsibilities":

                job.responsibilities,


        }



    # ==================================================
    # Knowledge Serialization
    # ==================================================

    def _serialize_knowledge(
        self,
        context: OptimizationContext,
    ) -> dict[str, Any]:

        knowledge = context.knowledge


        return {

            "target_role":

                knowledge.target_role,


            "missing_skills":

                knowledge.missing_skills,


            "matched_skills":

                knowledge.matched_skills,


            "priorities":

                knowledge.prioritized_skills,


            "categories":

                knowledge.skill_categories,


        }



    # ==================================================
    # Safety Budget
    # ==================================================

    def _calculate_word_budget(
        self,
        text: str,
    ) -> int:
        """
        Prevent AI paragraph expansion.

        Formula:

            original words × 1.35

        """

        words = len(
            text.split()
        )


        return max(

            5,

            int(
                words * 1.35
            ),

        )