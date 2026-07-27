from __future__ import annotations

from app.engine.models.document import (
    Document,
)
from app.engine.models.skill_priority import (
    SkillPriority,
)
from app.engine.models.promotion_plan import (
    PromotionDecision,
)


class EvidenceFinder:
    """
    Searches the resume for evidence that
    supports promoting a missing skill.

    No AI.

    Pure document analysis.
    """

    MIN_CONFIDENCE = 0.60

    @classmethod
    def find(

        cls,

        document: Document,

        missing_skills: list[SkillPriority],

    ) -> list[PromotionDecision]:

        resume_text = "\n".join(

            paragraph.text.lower()

            for paragraph in document.paragraphs

        )

        decisions = []

        for skill in missing_skills:

            tokens = [

                token.lower()

                for token in skill.skill.split()

            ]

            matched = sum(

                token in resume_text

                for token in tokens

            )

            confidence = (

                matched / len(tokens)

                if tokens else 0

            )

            evidence = (

                confidence >= cls.MIN_CONFIDENCE

            )

            decisions.append(

                PromotionDecision(

                    skill=skill.skill,

                    category=skill.category,

                    evidence_found=evidence,

                    confidence=round(
                        confidence,
                        2,
                    ),

                    reason=(
                        "Resume contains supporting evidence."
                        if evidence
                        else "Insufficient evidence."
                    ),

                )

            )

        return decisions