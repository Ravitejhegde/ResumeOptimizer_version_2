class RewritePromptBuilder:
    """
    Builds the AI prompt for rewriting
    a single resume paragraph.
    """

    @classmethod
    def build(
        cls,
        paragraph,
        optimization_plan,
        job_description,
    ) -> str:

        return f"""
You are an ATS resume optimization expert.

Job Description:
{job_description}

Optimization Plan:
{optimization_plan}

Resume Paragraph:
{paragraph.text}

Instructions:

- Preserve facts.
- Do not invent experience.
- Improve ATS keywords.
- Improve grammar.
- Keep approximately the same length.
- Return ONLY the rewritten paragraph.
"""