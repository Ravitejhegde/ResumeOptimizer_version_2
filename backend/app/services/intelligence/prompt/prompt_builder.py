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
    Builds the Brain v3 prompt.
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

        reasoning = getattr(
            context,
            "reasoning",
            None,
        )

        matched = []
        missing = []
        recommendations = []
        risks = []

        if reasoning:

            matched = reasoning.matched

            missing = [
                gap.name
                for gap in reasoning.missing
            ]

            recommendations = [

                recommendation.description

                for recommendation

                in reasoning.recommendations

            ]

            risks = [

                risk.description

                for risk

                in reasoning.risks

            ]

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
- Never change education.
- Never modify dates.
- Never create fake technologies.
- Rewrite only editable blocks.
- Preserve paragraph count.
- Preserve formatting.
- Return ONLY valid JSON.

==============================
OUTPUT FORMAT
==============================

{{
    "version": 3,
    "blocks": [
        {{
            "id": 1,
            "status": "updated",
            "text": "Updated paragraph"
        }}
    ]
}}
"""