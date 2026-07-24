from app.services.ai.provider.openrouter_provider import (
    OpenRouterProvider,
)

from app.services.intelligence.skills.technology_selector import (
    TechnologySelector,
)

from app.services.intelligence.skills.category_builder import (
    CategoryBuilder,
)

from app.services.intelligence.skills.line_budget import (
    LineBudget,
)

from app.services.intelligence.skills.skills_prompt_builder import (
    SkillsPromptBuilder,
)

from app.services.intelligence.skills.skills_response_parser import (
    SkillsResponseParser,
)


class SkillsOptimizer:
    """
    Complete Skills optimization pipeline.
    """

    provider = OpenRouterProvider()

    @classmethod
    def optimize(
        cls,
        resume_categories,
        jd_skills,
        selected_skills,
        target_role,
        max_lines,
    ):

        # -------------------------------------
        # Select Technologies
        # -------------------------------------

        technologies = TechnologySelector.select(
    resume_categories=resume_categories,
    jd_skills=jd_skills,
    selected_skills=selected_skills,
    target_role=target_role,
)

        # -------------------------------------
        # Build Categories
        # -------------------------------------

        categories = CategoryBuilder.build(
            technologies
        )

        # -------------------------------------
        # Apply Line Budget
        # -------------------------------------

        categories = LineBudget.apply(
            categories,
            max_lines,
        )

        # -------------------------------------
        # Build AI Prompt
        # -------------------------------------

        prompt = SkillsPromptBuilder.build(
            categories,
            target_role,
            max_lines,
        )

        # -------------------------------------
        # AI Optimization
        # -------------------------------------

        response = cls.provider.generate(
            prompt
        )
        print()
        print("=" * 60)
        print("AI SKILLS RESPONSE")
        print("=" * 60)
        print(response)
        print("=" * 60)
        # -------------------------------------
        # Parse Response
        # -------------------------------------

        return SkillsResponseParser.parse(
            response
        )