class PromptBuilder:

    @staticmethod
    def build(
        paragraph: str,
        job_description: str,
    ) -> str:

        return f"""
You are an expert ATS Resume Writer.

Your task is to improve ONE resume paragraph.

Rules:

- Never invent experience.
- Never invent projects.
- Never invent certifications.
- Never invent companies.
- Never change facts.
- Improve grammar.
- Use stronger action verbs.
- Add relevant ATS keywords naturally.
- Keep approximately the same visual length.
- Return ONLY the rewritten paragraph.

Job Description:

{job_description}

Resume Paragraph:

{paragraph}
"""