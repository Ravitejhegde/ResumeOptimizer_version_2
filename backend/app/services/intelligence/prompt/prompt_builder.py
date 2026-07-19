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
    Builds the final LLM prompt from PromptContext.
    """

    @classmethod
    def build(
        cls,
        context: PromptContext,
    ) -> str:

        # ------------------------------------------
        # System Prompt
        # ------------------------------------------

        system_prompt = SystemPrompt.build()

        # ------------------------------------------
        # Role-specific Optimization Rules
        # ------------------------------------------

        optimization_rules = OptimizationRules.build(
            context.plan.source_role,
            context.plan.target_role,
        )

        # ------------------------------------------
        # Final Prompt
        # ------------------------------------------

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
RESUME FACTS
==============================

Source Role:
{context.plan.source_role}

Target Role:
{context.plan.target_role}

==============================
KEEP TECHNOLOGIES
==============================

{json.dumps(context.keep, indent=2)}

==============================
REMOVE TECHNOLOGIES
==============================

{json.dumps(context.remove, indent=2)}

==============================
ADD TECHNOLOGIES
==============================

{json.dumps(context.add, indent=2)}

==============================
WARNINGS
==============================

{json.dumps(context.warnings, indent=2)}

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
OUTPUT FORMAT
==============================

Return ONLY valid JSON.

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