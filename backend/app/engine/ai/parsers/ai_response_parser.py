from __future__ import annotations

import json
import logging
from typing import Any

from app.engine.ai.models.ai_response import (
    AIOptimizationResponse,
)

from app.engine.ai.models.section_rewrite import (
    SectionRewrite,
)


logger = logging.getLogger(__name__)


class AIResponseParser:
    """
    Parses AI optimization response.

    New architecture:

        OpenRouter
             |
             v
        JSON Response
             |
             v
        AIResponseParser
             |
             v
    AIOptimizationResponse
             |
             v
        AIResponseMapper
             |
             v
        Writer


    Supports:

        - Paragraph based rewrites
        - Skills optimization
        - Summary optimization
        - Safe JSON extraction


    Does NOT:

        - Validate AI quality.
        - Modify DOCX.
    """



    def parse(
        self,
        raw_response: str,
    ) -> AIOptimizationResponse:


        data = self._load_json(
            raw_response
        )


        response = AIOptimizationResponse()



        # ----------------------------------
        # Basic fields
        # ----------------------------------

        response.title = (
            data.get("candidate_name")
            or
            data.get("title")
        )


        response.summary = (
            data.get("summary")
        )



        # ----------------------------------
        # Paragraph rewrites
        # ----------------------------------

        response.paragraphs = (
            self._parse_paragraphs(
                data.get(
                    "paragraphs",
                    [],
                )
            )
        )



        # ----------------------------------
        # Skills
        # ----------------------------------

        skills = data.get(
            "skills",
            {},
        )


        if isinstance(
            skills,
            dict,
        ):

            response.skills = skills



        # ----------------------------------
        # Metadata
        # ----------------------------------

        response.optimization_notes = (
            data.get(
                "optimization_notes",
                [],
            )
        )


        response.preserved_fields = (
            data.get(
                "preserved_fields",
                [],
            )
        )


        response.confidence = float(

            data.get(
                "confidence",
                0.0,
            )

        )



        logger.info(

            "[AIResponseParser] "
            "paragraphs=%s",

            len(
                response.paragraphs
            ),

        )


        return response



    # ==================================================
    # Paragraph parser
    # ==================================================

    def _parse_paragraphs(
        self,
        items: Any,
    ) -> list[SectionRewrite]:

        result: list[SectionRewrite] = []


        if not isinstance(
            items,
            list,
        ):

            return result



        for item in items:


            if not isinstance(
                item,
                dict,
            ):

                continue



            optimized = item.get(
                "optimized_text"
            )


            if not optimized:

                continue



            result.append(

                SectionRewrite(

                    section_type=item.get(
                        "section",
                        "paragraph",
                    ),

                    identifier=item.get(
                        "paragraph_id"
                    ),

                    original_text=item.get(
                        "original_text"
                    ),

                    optimized_text=optimized,

                    reason=item.get(
                        "reason"
                    ),

                    confidence=float(

                        item.get(
                            "confidence",
                            0.0,
                        )

                    ),

                )

            )


        return result



    # ==================================================
    # JSON Loader
    # ==================================================

    def _load_json(
        self,
        text: str,
    ) -> dict[str, Any]:


        try:

            return json.loads(
                text
            )


        except json.JSONDecodeError:


            logger.warning(

                "[AIResponseParser] "
                "Direct JSON parsing failed."

            )


            cleaned = (
                self._extract_json(
                    text
                )
            )


            return json.loads(
                cleaned
            )



    # ==================================================
    # JSON extraction
    # ==================================================

    @staticmethod
    def _extract_json(
        text: str,
    ) -> str:
        """
        Extract JSON from markdown wrapped output.
        """


        start = text.find(
            "{"
        )


        end = text.rfind(
            "}"
        )


        if (
            start == -1
            or
            end == -1
        ):

            raise ValueError(
                "No JSON object found."
            )


        return text[
            start:end + 1
        ]