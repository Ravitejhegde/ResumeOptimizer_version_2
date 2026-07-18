import json

from app.services.docx.document_block import DocumentBlock
from app.services.jd.technology_promoter import (
    TechnologyPromotion,
)
from app.services.knowledge.resume_knowledge import (
    ResumeKnowledge,
)


class BatchPromptBuilder:

    @staticmethod
    def build(
        blocks: list[DocumentBlock],
        knowledge: ResumeKnowledge,
        promotion: TechnologyPromotion,
        job_description: str,
    ) -> str:

        knowledge_json = {
            "frontend": sorted(knowledge.frontend),
            "backend": sorted(knowledge.backend),
            "database": sorted(knowledge.database),
            "programming_languages": sorted(
                knowledge.programming_languages
            ),
            "cloud": sorted(knowledge.cloud),
            "devops": sorted(knowledge.devops),
            "tools": sorted(knowledge.tools),
        }

        # --------------------------------------------------
        # Only send editable blocks to AI
        # --------------------------------------------------

        editable_blocks = []

        for block in blocks:

            if not block.can_optimize:
                continue

            editable_blocks.append(

                {
                    "id": block.id,
                    "type": block.block_type,
                    "text": block.text,
                }

            )

        prompt = f"""
You are ResumeOptimizer AI.

You are editing an existing professional resume.

IMPORTANT RULES

GENERAL

- Edit ONLY the supplied editable blocks.
- Never create new blocks.
- Never change block IDs.
- Never change section headings.
- Never invent experience.
- Never invent companies.
- Never invent projects.
- Never invent certifications.
- Never invent employment dates.
- Never invent achievements.
- Never invent technologies that are not provided.

OPTIMIZATION

- Prioritize ONLY technologies listed under "selected_missing".
- Ignore missing technologies that are not listed.
- Improve ATS score naturally.
- Keep approximately the same paragraph length.
- Preserve the writing style.
- Preserve factual information.
- Preserve the original meaning.
- Do not make paragraphs significantly longer.

OUTPUT

- Return VALID JSON ONLY.
- Return only updated blocks.


{job_description}

Resume Knowledge

{json.dumps(knowledge_json, indent=2)}

Optimization Targets

{json.dumps({
    "matched": promotion.promote,
    "selected_missing": promotion.missing,
    "extra": promotion.extra,
}, indent=2)}

Editable Resume Blocks

{json.dumps(editable_blocks, indent=2)}

Return exactly:

{{
  "version": 2,
  "blocks": [
    {{
      "id": 1,
      "status": "updated",
      "text": "Improved paragraph"
    }}
  ]
}}
"""

        return prompt