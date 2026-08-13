"""
app.optimizer.prompts.resume_prompt

Builds the resume context prompt.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)

from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


def build_resume_prompt(
    document: DocumentModel,
    resume: ResumeUnderstanding,
) -> str:
    """
    Build the resume context for AI.

    Includes:
    - Resume understanding
    - Original resume paragraphs

    This gives the AI enough context to
    safely rewrite individual paragraphs.
    """

    sections: list[str] = []

    # ----------------------------------
    # Resume Understanding
    # ----------------------------------

    sections.append(
        f"""
RESUME UNDERSTANDING

Primary Role:
{resume.primary_role}

Secondary Roles:
{", ".join(resume.secondary_roles)}

Primary Skills:
{", ".join(resume.primary_skills)}

Primary Technologies:
{", ".join(resume.primary_technologies)}

Strongest Experience:
{resume.strongest_experience}

Strongest Project:
{resume.strongest_project}

Strengths:
{", ".join(resume.strengths)}

Weaknesses:
{", ".join(resume.weaknesses)}

Seniority:
{resume.seniority}

Professional Summary:
{resume.summary}
""".strip()
    )

    # ----------------------------------
    # Original Resume
    # ----------------------------------

    sections.append("")

    sections.append("ORIGINAL RESUME")

    for index, paragraph in enumerate(
        document.paragraphs,
        start=1,
    ):

        if not paragraph.strip():
            continue

        sections.append(
            f"""
Paragraph ID: p{index}

Text:
{paragraph}
""".strip()
        )

    # ----------------------------------
    # Rules
    # ----------------------------------

    sections.append(
        """
RULES

Use ONLY the information contained in the
resume.

Do NOT invent experience.

Do NOT invent projects.

Do NOT invent technologies.

Do NOT invent certifications.

Only improve wording, clarity,
ATS alignment, and keyword usage.
""".strip()
    )

    return "\n\n".join(
        sections
    )