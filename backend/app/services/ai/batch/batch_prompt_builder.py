class BatchPromptBuilder:
    """
    Builds high-quality prompts for rewriting
    resume paragraphs while preserving truth,
    formatting, and ATS relevance.
    """

    @classmethod
    def build(
        cls,
        paragraphs,
        optimization_plan,
        job_description,
    ) -> str:

        keep = ", ".join(
            map(
                str,
                getattr(
                    optimization_plan,
                    "keep",
                    [],
                ),
            )
        )

        add = ", ".join(
            map(
                str,
                getattr(
                    optimization_plan,
                    "add",
                    [],
                ),
            )
        )

        remove = ", ".join(
            map(
                str,
                getattr(
                    optimization_plan,
                    "remove",
                    [],
                ),
            )
        )

        warnings = "\n".join(
            getattr(
                optimization_plan,
                "warnings",
                [],
            )
        )

        prompt = f"""
You are a senior ATS Resume Optimization Expert.

Your task is to rewrite ONLY the supplied resume paragraphs.

==================================================
JOB DESCRIPTION
==================================================

{job_description}

==================================================
OPTIMIZATION PLAN
==================================================

Keep Skills:
{keep}

Add Skills:
{add}

Remove Skills:
{remove}

Warnings:
{warnings}

==================================================
OBJECTIVE
==================================================

Rewrite the supplied resume paragraphs so they
better match the Job Description while remaining
100% truthful.

==================================================
STRICT RULES
==================================================

1. NEVER invent work experience.

2. NEVER invent projects.

3. NEVER invent companies.

4. NEVER invent education.

5. NEVER invent certifications.

6. NEVER invent dates.

7. NEVER claim experience with technologies
the candidate has never used.

8. Add only relevant ATS keywords naturally.

9. Preserve the original meaning.

10. Preserve approximately the same paragraph length.

11. Improve grammar and readability.

12. Do NOT use Markdown.

13. Do NOT use bullet points unless the original
paragraph already contains bullets.

14. Return ONLY a valid JSON object.

15. Do NOT include explanations.

16. Do NOT include code fences.

17. The response must start with "{{" and end with "}}".

==================================================
OUTPUT FORMAT
==================================================

Return ONLY this JSON object.

{{
    "P00001": "rewritten paragraph",
    "P00002": "rewritten paragraph"
}}

Do not write anything before or after the JSON.

==================================================
PARAGRAPHS
==================================================
"""

        for paragraph in paragraphs:

            prompt += f"""

----------------------------------------

Paragraph ID:
{paragraph.id}

Original Text:

{paragraph.text}

"""

        return prompt