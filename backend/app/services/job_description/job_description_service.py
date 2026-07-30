from __future__ import annotations

import logging

from app.engine.analyzer.analyzers.job_description_analyzer import (
    JobDescriptionAnalyzer,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


logger = logging.getLogger(__name__)


class JobDescriptionService:
    """
    Application service for job description analysis.

    Flow:

        API
          |
          v
        Service
          |
          v
        JobDescriptionAnalyzer
          |
          v
        KnowledgeManager


    Responsibilities:
        - Initialize dependencies.
        - Coordinate JD analysis.

    Does not:
        - Extract skills itself.
        - Detect technologies itself.
        - Contain analysis logic.
    """


    def __init__(self) -> None:

        self._knowledge = KnowledgeManager()

        self._knowledge.initialize()

        self._analyzer = JobDescriptionAnalyzer(
            self._knowledge,
        )


    # --------------------------------------------------
    # Analyze
    # --------------------------------------------------

    def analyze(
        self,
        job_description: str,
    ) -> dict:

        result = self._analyzer.analyze(
            job_description,
        )


        logger.info(
            "Job description analyzed successfully."
        )


        return {

            "role": result.role,

            "required_skills": (
                result.required_skills
            ),

            "preferred_skills": (
                result.preferred_skills
            ),

            "keywords": (
                result.keywords
            ),

            "minimum_experience": (
                result.minimum_experience
            ),

        }