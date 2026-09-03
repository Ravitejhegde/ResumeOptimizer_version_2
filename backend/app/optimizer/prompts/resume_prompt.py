"""
app.optimizer.prompts.resume_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    ):
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

Use the resume as the factual source.

Matched skills may be strengthened
when relevant to the existing resume content.

User-selected missing skills are explicitly
authorized by the user and may be incorporated
into the resume.

User-selected missing skills must NOT be used
to invent experience, projects, achievements,
responsibilities, certifications, employment
history, or measurable results.

Do NOT add missing skills that were not
selected by the user.

Do NOT invent experience.

Do NOT invent projects.

Do NOT invent certifications.

Do NOT invent achievements.

Do NOT invent responsibilities.

Do NOT invent employment history.

Only improve wording, clarity, ATS alignment,
and keyword usage while following the
optimization plan.
""".strip()
    )

    return "\n\n".join(
        sections
    )