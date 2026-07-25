import json

from app.services.intelligence.prompt.prompt_context import (
    PromptContext,
)

from app.services.intelligence.prompt.system_prompt import (
    SystemPrompt,
)

from app.services.intelligence.prompt.optimization_rules import (
    OptimizationRules,
)


class PromptBuilder:
    """
    Builds the ResumeOptimizer AI prompt.
    """

    @classmethod
    def build(
        cls,
        context: PromptContext,
    ) -> str:

        system_prompt = SystemPrompt.build()

        optimization_rules = OptimizationRules.build(
            context.plan.source_role,
            context.plan.target_role,
        )

        matched = context.plan.keep
        missing = context.plan.add
        recommendations = context.plan.selected_skills
        risks = context.plan.warnings

        return f"""
==============================
SYSTEM PROMPT
==============================

{system_prompt}

==============================
OPTIMIZATION RULES
==============================

{optimization_rules}

==============================
ROLE TRANSITION
==============================

Source Role:
{context.plan.source_role}

Target Role:
{context.plan.target_role}

==============================
MATCHED SKILLS
==============================

{json.dumps(matched, indent=2)}

==============================
MISSING SKILLS
==============================

{json.dumps(missing, indent=2)}

==============================
RECOMMENDATIONS
==============================

{json.dumps(recommendations, indent=2)}

==============================
RISKS
==============================

{json.dumps(risks, indent=2)}

==============================
FORMATTING RULES
==============================

{context.formatting_rules}

==============================
JOB DESCRIPTION
==============================

{context.job_description}

==============================
EDITABLE BLOCKS
==============================

{json.dumps(context.blocks, indent=2)}

==============================
STRICT INSTRUCTIONS
==============================

- Never invent work experience.
- Never invent companies.
- Never modify education.
- Never modify dates.
- Never invent technologies.
- Rewrite ONLY editable content.
- Preserve document structure.
- Preserve paragraph count.
- Preserve formatting.
- Preserve run order.
- Do not create new runs.
- Do not remove runs.
- Never modify hyperlinks.
- Never modify URLs.
- Never modify bookmarks.
- Never modify comments.
- Never modify hidden fields.
- Never modify images.
- Return ONLY valid JSON.

==============================
OUTPUT FORMAT
==============================

{{
  "version": 4,
  "blocks": [
    {{
      "id": 1,
      "status": "updated",
      "runs": [
        {{
          "index": 0,
          "text": "Updated editable run"
        }},
        {{
          "index": 3,
          "text": "Another updated editable run"
        }}
      ]
    }}
  ]
}}

==============================
IMPORTANT
==============================

- Return ONLY valid JSON.
- Do not wrap the JSON inside markdown.
- Return ONLY editable runs.
- Never return hyperlinks.
- Never return URLs.
- Never return images.
- Never return bookmarks.
- Never return comments.
- Never return hidden fields.
- Never return locked runs.
- Keep run indexes unchanged.
- Preserve run order.
- Update ONLY the text of editable runs.
"""