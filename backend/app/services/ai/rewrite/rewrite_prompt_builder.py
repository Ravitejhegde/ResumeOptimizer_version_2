class RewritePromptBuilder:
    """
    Builds a high-quality prompt for rewriting
    one resume paragraph.
    """

    @classmethod
    def build(
        cls,
        paragraph,
        optimization_plan,
        job_description,
    ) -> str:

        keep = ", ".join(
            getattr(optimization_plan, "keep", [])
        )

        add = ", ".join(
            getattr(optimization_plan, "add", [])
        )

        remove = ", ".join(
            getattr(optimization_plan, "remove", [])
        )

        warnings = "\n".join(
            getattr(optimization_plan, "warnings", [])
        )

        return f"""
You are an expert ATS Resume Writer.

Your job is to improve ONE resume paragraph.

========================
JOB DESCRIPTION
========================

{job_description}

========================
OPTIMIZATION PLAN
========================

Keep:
{keep}

Add:
{add}

Remove:
{remove}

Warnings:
{warnings}

========================
RESUME PARAGRAPH
========================

{paragraph.text}

========================
RULES
========================

1. Never invent experience.

2. Never change company names.

3. Never change dates.

4. Never change project names.

5. Improve ATS keywords naturally.

6. Improve grammar.

7. Improve readability.

8. Keep approximately the same length.

9. Preserve the original meaning.

10. Return ONLY the rewritten paragraph.

Do not use Markdown.
Do not explain your answer.
"""