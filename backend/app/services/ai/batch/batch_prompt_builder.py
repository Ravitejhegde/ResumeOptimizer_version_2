class BatchPromptBuilder:
    """
    Builds a single prompt containing
    multiple resume paragraphs.
    """

    @classmethod
    def build(
        cls,
        paragraphs,
        optimization_plan,
        job_description,
    ) -> str:

        prompt = f"""
You are an expert ATS Resume Writer.

JOB DESCRIPTION

{job_description}

OPTIMIZATION PLAN

{optimization_plan}

Rewrite the following resume paragraphs.

Rules:

- Preserve facts.
- Do NOT invent experience.
- Improve ATS keywords.
- Improve grammar.
- Preserve paragraph order.
- Return ONLY JSON.

JSON FORMAT

{{
    "P00001":"updated text",
    "P00002":"updated text"
}}

PARAGRAPHS

"""

        for paragraph in paragraphs:

            prompt += f"""

ID: {paragraph.id}

TEXT:
{paragraph.text}

"""

        return prompt