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
    authorized_paragraph_ids: set[str] | None = None,
) -> str:
    """
    Build the resume context for AI.

    Includes:
    - Resume understanding
    - Authorized original resume paragraphs
    - Resume safety rules

    Empty Resume Understanding fields are omitted
    to reduce unnecessary prompt tokens.
    """

    sections: list[str] = []

    # ----------------------------------
    # Resume Understanding
    # ----------------------------------

    understanding_lines: list[str] = [
        "RESUME UNDERSTANDING"
    ]

    if resume.primary_role:
        understanding_lines.append(
            f"Primary Role: {resume.primary_role}"
        )

    if resume.secondary_roles:
        understanding_lines.append(
            "Secondary Roles: "
            + ", ".join(resume.secondary_roles)
        )

    if resume.primary_skills:
        understanding_lines.append(
            "Primary Skills: "
            + ", ".join(resume.primary_skills)
        )

    if resume.primary_technologies:
        understanding_lines.append(
            "Primary Technologies: "
            + ", ".join(resume.primary_technologies)
        )

    if resume.strongest_experience:
        understanding_lines.append(
            f"Strongest Experience: "
            f"{resume.strongest_experience}"
        )

    if resume.strongest_project:
        understanding_lines.append(
            f"Strongest Project: "
            f"{resume.strongest_project}"
        )

    if resume.strengths:
        understanding_lines.append(
            "Strengths: "
            + ", ".join(resume.strengths)
        )

    if resume.weaknesses:
        understanding_lines.append(
            "Weaknesses: "
            + ", ".join(resume.weaknesses)
        )

    if resume.seniority:
        understanding_lines.append(
            f"Seniority: {resume.seniority}"
        )

    if resume.summary:
        understanding_lines.append(
            f"Professional Summary: {resume.summary}"
        )

    sections.append(
        "\n".join(understanding_lines)
    )

    # ----------------------------------
    # Original Resume
    # ----------------------------------

    sections.append("ORIGINAL RESUME")

    for index, paragraph in enumerate(
        document.paragraphs,
    ):
        paragraph_id = f"p{index}"

        if (
            authorized_paragraph_ids is not None
            and paragraph_id not in authorized_paragraph_ids
        ):
            continue

        sections.append(
            f"""
Paragraph ID: {paragraph_id}

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

    return "\n\n".join(sections)