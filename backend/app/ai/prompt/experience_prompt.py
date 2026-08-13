"""
app.ai.prompt.experience_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds AI prompts for optimizing resume experience.
"""

from __future__ import annotations

from app.analyzer.models.experience_model import (
    ExperienceModel,
)
from app.planner.blueprint.optimization_blueprint import (
    OptimizationBlueprint,
)


class ExperiencePrompt:
    """
    Builds prompts for experience optimization.
    """

    def build(
        self,
        experience: ExperienceModel,
        blueprint: OptimizationBlueprint,
    ) -> str:
        """
        Build a production-ready prompt for the AI.
        """

        description = "\n".join(
            experience.description
        )

        return f"""
You are an expert ATS Resume Writer.

Your task is to improve ONLY the experience section below.

STRICT RULES

1. Never invent:
   - companies
   - projects
   - technologies
   - achievements
   - certifications
   - dates

2. Never exaggerate experience.

3. Preserve the original meaning.

4. Improve ATS keyword usage.

5. Improve grammar.

6. Improve readability.

7. Use strong action verbs.

8. Keep bullet points concise.

9. Return ONLY rewritten bullet points.

10. Do NOT use markdown.

Target Role:
{blueprint.goal.target_role}

Optimization Goal:
{blueprint.goal.objective}

Rewrite Strategy:
{blueprint.rewrite_plan.global_strategy}

Original Experience

Title:
{experience.title}

Company:
{experience.company}

Duration:
{experience.duration}

Description:
{description}
""".strip()